# ButtonCtl
<div style="text-align:center"><img src="./buttons-platzierung.png" /></div>

### dependencies
- RPi python3-rpi.gpio
```bash
sudo apt install python3-rpi-gpio
```
- OpenSSH client
```bash
sudo apt install openssh
```
- circuitpython libraries for neopixel
```bash
pip3 install adafruit-circuitpython-neopixel
```

### install
```bash
git clone https://github.com/dylangoepel/buttonctl.git
cd buttonctl
./service.sh # create systemd .service file
sudo systemctl enable buttond # autostart at boot
sudo systemctl start buttond # start as daemon
```

### wiring
- pin 23: left button input (pull-down)
- pin 24: center button input (pull-down)
- pin 22: right button input (pull-down)
- pin 18: neopixel data
- pin 4: (pull-down)

![](pins.png)

- led strip:
```
(25-36)  (13-24)  (1-12)
 AERIE            KELLER

 (counter-clockwise)
```

### usage
![Rot](https://placehold.it/15/ff0000/000000?text=+)
![Schwarz](https://placehold.it/15/000000/000000?text=+)
![Rot](https://placehold.it/15/ff0000/000000?text=+)
→ Linker Button

![Schwarz](https://placehold.it/15/000000/000000?text=+)
![Grün](https://placehold.it/15/00ff00/000000?text=+)
![Rot](https://placehold.it/15/ff0000/000000?text=+) 
→ Mittlerer Button

![Rot](https://placehold.it/15/ff0000/000000?text=+)
![Schwarz](https://placehold.it/15/000000/000000?text=+)
![Rot](https://placehold.it/15/ff0000/000000?text=+)
→ Kurze Wartezeit

![Grün](https://placehold.it/15/00ff00/000000?text=+)
![Schwarz](https://placehold.it/15/000000j/000000?text=+)
![Rot](https://placehold.it/15/ff0000/000000?text=+) 

----------

![Rot](https://placehold.it/15/ff0000/000000?text=+)
![Schwarz](https://placehold.it/15/000000/000000?text=+)
![Rot](https://placehold.it/15/ff0000/000000?text=+)
→ Linker Button

![Schwarz](https://placehold.it/15/000000/000000?text=+)
![Grün](https://placehold.it/15/00ff00/000000?text=+)
![Rot](https://placehold.it/15/ff0000/000000?text=+) 
→ Linker Button

![Rot](https://placehold.it/15/ff0000/000000?text=+)
![Schwarz](https://placehold.it/15/000000/000000?text=+)
![Rot](https://placehold.it/15/ff0000/000000?text=+)

-----------

![Rot](https://placehold.it/15/ff0000/000000?text=+)
![Schwarz](https://placehold.it/15/000000/000000?text=+)
![Rot](https://placehold.it/15/ff0000/000000?text=+)
→ Mittlerer Button

![Rot](https://placehold.it/15/ff0000/000000?text=+)
![Schwarz](https://placehold.it/15/000000/000000?text=+)
![Rot](https://placehold.it/15/ff0000/000000?text=+)
