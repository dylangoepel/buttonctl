import time

start = time.time()
import RPi.GPIO as gpio
from neopixel import NeoPixel, GRB
from board import D18
from json import loads
from urllib.request import urlopen
from os.path import expanduser
from os import system
import threading

print("Imports took", round(time.time() - start, 2), "seconds")


def ssh_(host, name):
    print("[ssh]", host, name)
    system("ssh " + str(name) + "@" + host)

def ssh(host, name):
    threading.Thread(target=ssh_, args=(host, name)).start()



class Door:
    def __init__(self, host, users):
        self.host = host
        self.users = users

    def open(self):
        ssh(self.host, self.users[0])

    def close(self):
        ssh(self.host, self.users[1])


class ButtonStrip:
    def __init__(self, strip, leds):
        self.leds = leds
        self.strip = strip

    def draw(self, color):
        for led in self.leds:
            self.strip[led] = color


class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=100):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = gpio.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = gpio.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()


class ButtonSensor:
    def __init__(self, pin, callback):
        self.pin = pin

        gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        self.handler = ButtonHandler(pin, callback,
                                     edge='falling', bouncetime=100)
        self.handler.start()
        gpio.add_event_detect(pin, gpio.BOTH, callback=self.handler)


class ButtonPress(Exception):
    def __init__(self, pin):
        Exception.__init__(self)
        self.pin = pin

    def __str__(self):
        return buttons[self.pin]


class MultiSensor:
    def __init__(self, pins):
        self.buttons = []
        self.pressed = None
        for pin in pins:
            self.buttons.append(ButtonSensor(pin, self.press))

    def press(self, pin):
        self.pressed = pin

    def sleepSecond(self):
        for i in range(100):
            if self.pressed is not None:
                pressedPin = self.pressed
                self.pressed = None
                raise ButtonPress(pressedPin)
            time.sleep(0.01)

    def sleep(self, delay):
        for i in range(delay):
            self.sleepSecond()


class APILoader:
    def __init__(self, delay):
        self.delay = delay
        self.loadData()

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def getData(self):
        return self.data

    def run(self):
        while True:
            try:
                self.loadData()
            except Exception as e:
                print("Unable to load API data:", e)

            time.sleep(self.delay)

    def loadData(self):
        # Load api data
        response = urlopen("https://status.chaospott.de/api/").read()
        data = loads(response.decode("utf-8"))

        self.data = {door["location"]: not door["value"]
                     for door in data["sensors"]["door_locked"]}




print("[*] Initializing...")
# Initialize GPIO board
gpio.setmode(gpio.BCM)

# Create LED-Strip handle
gpio.setup(4, gpio.IN, pull_up_down=gpio.PUD_UP)
strip = NeoPixel(D18, 36, brightness=0.5,
                          pixel_order=GRB, auto_write=False)

# Create subhandles for each button handles
leds = {
        "cellar": ButtonStrip(strip, list(range(1, 12))),
        "center": ButtonStrip(strip, list(range(12, 24))),
        "aerie": ButtonStrip(strip, list(range(24, 36))),
}

# Create button press sensor
buttons = {
        22: "cellar",
        23: "aerie",
        24: "center",
}
sensor = MultiSensor([i for i in buttons])

doors = {
        "aerie": Door("10.42.1.28", ("open", "close")),
        "cellar": Door("10.42.1.20", ("unlock", "lock")),
}

# Initialize API interface
loader = APILoader(4)
loader.start()

print("[*] Starting...")
while True:
    for led in leds:
        leds[led].draw((0, 0, 0))

    data = loader.getData()
    for door in data:
        if door in leds:
            leds[door].draw((0, 255, 0) if data[door] else (255, 0, 0))

    strip.show()

    # Wait for a button press
    try:
        sensor.sleep(2)
    except ButtonPress as press:
        selection = str(press)

        if selection == "aerie":
            leds["cellar"].draw((255, 0, 0))
        elif selection == "cellar":
            leds["aerie"].draw((255, 0, 0))
        else:
            continue

        leds[selection].draw((0, 0, 0))
        leds["center"].draw((0, 255, 0))

        strip.show()

        try:
            sensor.sleep(5)
        except ButtonPress as press:
            action = str(press)
            
            if action == "center":
                target=doors[selection].open()
            elif action != selection:
                doors[selection].close()
