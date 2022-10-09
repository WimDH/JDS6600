# About the Project
The JDS6600 is a 2-channel DDS signal generator with a built-in frequency counter. It comes in a few flafours, one cam generate signals up to 60MHz, the lite version only up to 15MHz
The Signal generator can be controlled via a USB port, and via the control panel.
This module makes it easier to control the signal generator via the USB port. It abstacts most of 
functions offered via the remote control.
The documentation I have found on the internmanufacturer's website (https://joy-it.net/de/products/JT-JDS6600), is not very clear and it seems that not all options which are available via manual control, are possible via the remote control.
I've also found out the the sgnal generator was available from another company, called Hangzou Junce Instruments. 
# Getting started
# Prerequisites
This python package is only supporting Python 3. The only external dependency is pyserial.
## Installation
The package can be installed with pip.
```
pip install jds6600
pip install jds6600[test]
```
# Quick start
## Open and close a connection
*Remark: Your USB port may be different.*

```
>>> import jds6600
>>> fg = jds6600.JDS6600(port="/dev/ttyUSB3")
>>> fg.connect()
<jds6600.core.JDS6600 object at 0x7f04a951ac50>
>>> print(fg.get_channels())
(False, False)
>>> fg.close()
```

Or using the with statement

```
>>> import jds6600
>>> with jds6600.JDS6600(port="/dev/ttyUSB3") as fg:
...     print(fg.get_channels())
... 
(False, False)
```

Available methods:

```
>>> fg.get_channels()
(False, False)
>>> fg.set_channels(channel1=True, channel2=True)
'ok'
>>> fg.get_waveform(channel=1)
'sine'
>>> fg.set_waveform(channel=1, value='triangle')
'ok'
>>> fg.get_frequency(channel=1)
0.0
>>> fg.set_frequency(channel=1, value=1e3)
'ok'
>>> fg.get_amplitude(channel=2)
5.0
>>> fg.set_amplitude(channel=1, value=1.23)
'ok'
>>> fg.get_offset(channel=1)
0.0
>>> fg.set_offset(channel=1, value=0.5)
'ok'
>>> fg.get_dutycycle(channel=1)
50.0
>>> fg.set_dutycycle(channel=1, value=20.1)
'ok'
```

# Contributing
If you want to contribute to this project, you're mostly welcome! Just keep a few thing in mind, and it will go smooth.
1. Fork the project
2. Create a branch (`git checkout -b myfeature`)
3. Check your code using `flake8` and `mypy`
4. Commit your changes (`git commit -m "added a nice feature"`)
5. Push your branch to github (`git push origin myfeature`)
6. Open a Pull Request 

# License
Distributed under the MIT License. See `LICENSE.txt` for more information.
