# WLedController

WLedController is an interface, which enables plain Python controll of your WLEDs.
It utilizes the native WLed json-API, for further information [check out their documentation](https://kno.wled.ge/interfaces/json-api/).

Since this library is currently under constant development, fell free to [submit feedback](https://github.com/tj0vtj0v/WLedController/issues) if there are issues or missing features.

## Getting Started
Here you find instructions how to install and use this library.

### Prerequisites
To run WLedController, you have to ensure
 - [WLed](https://kno.wled.ge/basics/getting-started/) and
 - [Python3](https://www.python.org) with
 - [requests](https://pypi.org/project/requests/)

is properly installed and set up.

#### via Pypi
```bash
> pip install WLedController
```

#### manually for all users
1. download the archive and unpack it.
2. enter the directory and run the setup script.
```bash
> python setup.py install
```

#### manually for a single user
1. download the archive and unpack it.
2. move the "WLedController" subfolder into the directory your script is located.

### Usage
To use WLedControll you have to create an Object with the correct IP-Adress of your Controller (ESP-32 in my case).
```python
from WLedController import WLedController

with WLedController(wled_ip_address=<IP-Address of WLED Controller>) as WLeds:
```
 - wled_ip_address is the IP-Address of your WLED Controller, to find this address
    - you can look up the connections in [fritz.box](https://fritz.box/),
    - or you install the Mobile-App 'WLED - native' on [Apple](https://apps.apple.com/de/app/wled-native/id6446207239) or [Android](https://play.google.com/store/apps/details?id=ca.cgagnier.wlednativeandroid&hl=gsw&gl=US).
