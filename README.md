# ButtonCtl
ButtonCTL im oberen Stockwerk des Chaospott zur vereinfachenden Steuerung der via SSH kontrollierbaren Türen mithilfe
von physischen Buttons genutzt. Er ersetzt ein gleichnamiges älteres System.
In seiner momentanen Version ist es nicht mit der zweiten Button-Installation neben der Kellertür
kompatibel, und kann dort somit nicht eingesetzt werden.

## Installation
### Software
Zur Installation der im nächsten Abschnitt besprochenen Abhängigkeiten öffnen sie zunächst eine Shell.
An diesem Punkt ist es ratsam das ihr System mit `sudo apt update && sudo apt upgrade`
zu aktualieren. Nun nutzen sie `sudo apt install python3-rpi-gpio` zur Installation der Python-RPi Library und
`sudo pip3 install adafruit-circuitpython-neopixel` zur Installation der ebenfalls notwendigen Neopixel-Library.

Des Weiteren wird ein SSH-Client mit einem auf dem Türsystem registrierten Schlüssel benötigt. Den SSH-Client
installieren sie auf einem Raspbian System mit `sudo apt install openssh`. Für weitere Informationen über den
benötigten Schlüssel sehen sie [hier](https://dokuwiki.chaospott.de/infrastruktur:zugang:start).

### Hardware
Zum Ausführen von ButtonCtl ist der korrekte Anschluss aller Komponenten notwendig. Um
die Verkabelung in der aktuellen Installation des Systems im Club zu verändern, öffnen sie
den unteren, in der rechts neben der Tür im Bällebad befindlichen  Wand verbauten Kasten.
Um den Raspberry Pi zu erreichen, müssen sie nun die dort verbauten Schrauben lösen, und die Abdeckung abnehmen.

<div style="text-align:center"><img src="./buttons-platzierung.png" /></div>

Das Programm kommuniziert mit dem LED-Strip über die Pins 7 (BCM 4) und 12 (BCM 18). Die Buttons sind den
Pins 23 (Aerie), 24 (Center), 22 (Keller) zugeordnet.

### Ausführen
Zum Ausführen klonen sie zuerst dieses Git-Repository.
```bash
git clone https://github.com/dylangoepel/buttonctl.git
cd buttonctl
```
Nun können sie entweder `button.py` direkt mit `python3 button.py` ausführen oder einen Systemd-Service erstellen, der
daraufhin automatisch beim Bootvorgang gestartet werden kann. Zum Erstellen des Services nutzen sie `bash service.sh`,
und zur Aktivierung des automatischen Starts daraufhin `systemctl enable buttond`.

## Abhängigkeiten
### Libraries
Zur Implementierung einiger zentraler Features werden folgende nicht-standard Libraries genutzt:
- RPi (raspbian: python3-rpi.gpio)
- neopixel (pypi: adafruit-circuitpython-neopixel)

Da die Buttons nicht etwa über einzelne LEDs, sondern über einen einzelnen LED-Strip angesteuert
werden müssen, wird die ```neopixel``` Library dazu genutzt, den aus 36 (3 * 12) Leds bestehenden Strip zu bedienen
und auf Basis dessen zu einem Button-orientierten Interface zu abstrahieren.
Die LEDs sind folgendermaßen über die Buttons verteilt:
```
(25-36)  (13-24)  (1-12)
 AERIE            KELLER
```

Um das dazu - und zur Button-Press Erkennung - benötigte GPIO-Board zu kontrollieren, nutzt ButtonCtl die ```RPi.gpio```
Library.

### API
ButtonCtl greift auf die vom Chaospott bereitgestellte [SpaceAPI](http://spaceapi.net/)-Instanz, die - wie es die
Spezifikation vorsieht - neben den benötigten Sensor-Daten ebenfalls allgemeine Information
sowie Metadaten über den Hackerspace überträgt, zurück.
Die Statusinformationen befinden sich im `sensor` Bereich der JSON-Daten:
```json
{
  "door_locked": [
    {
      "location": "aerie",
      "value": false
    },
    {
      "location": "cellar",
      "value": false
    }
  ]
}
```

### Türsteuerung
Zum Öffnen und Schließen der beiden Türen werden die jeweiligen SSH-Endpunkte genutzt:
- Keller
  - `ssh unlock@10.42.1.20`
  - `ssh lock@10.42.1.20`
- Aerie:  open / close @ 10.42.1.28
  - `ssh open@10.42.1.28`
  - `ssh close@10.42.1.28`
 
## Benutzung
Wie durch wiederholte Ausfälle indiziert, sind die durch die API bereitgestellten Daten nicht immer zuverlässig,
und sollen somit keinen Einfluss auf die Funktionalität der Buttons haben. In der Vergangenheit
erfolgte das Öffnen oder Schließen einer Tür durch einfaches Drücken auf den mit dieser assoziierten Knopf.
Unter der Voraussetzung, dass der gespeicherte Türstatus korrekt ist, wurde dieser dann geändert, das heißt die
Tür wurde geöffnet oder geschlossen.

Um jenes Vorgehen trotz der Unwissenheit über den aktuellen Zustand der Türen zu ermöglichen, leuchtet in der neuen
Version nach dem Drücken eines Türknopfes (1. / 3. Knopf für Aerie / Keller) ein Button grün und ein anderer rot auf.
Nach erneutem Drücken auf den grünen (roten) Button wird die Tür daraufhin geöffnet (geschlossen).

Im Normalzustand leuchtet der mittlere Button nicht und die Tür-Buttons tragen die mit ihrem API-Status
assoziierten Farben.

### Beispiele

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
