import json
from datetime import datetime
from time import sleep
from enum import Enum

import requests.exceptions

from exceptions import *


class Specifier(Enum):
    none = ""
    state = "state"
    info = "info"
    effects = "effects"
    palettes = "palettes"


class WLedController:
    def __init__(self, wled_ip_address: str) -> None:
        self.api_url = f"http://{wled_ip_address}/json/"
        self.log = True

        try:
            self.get_status()
        except:
            raise UnreachableAddressException(wled_ip_address)

    @staticmethod
    def _timestamp() -> str:
        return str(datetime.now())[:-7]

    @staticmethod
    def _build_data(*args: tuple[str: any]):
        return "{" + ", ".join([f'"{arg[0]}": {arg[1]}' for arg in args]) + "}"

    def _logging(self, msg: str):
        print(f"{self._timestamp()}: {msg}")

    def activate_log(self):
        self.log = True

    def deactivate_log(self):
        self.log = False

    def get_status(self, specification: Specifier = Specifier.none) -> dict:
        return requests.get(self.api_url + specification.value).json()

    def send_arguments(self, arguments: str):
        try:
            status = list(json.loads(requests.post(self.api_url, arguments).text))[0]

            if self.log:
                self._logging(f"{arguments} --> {status}")

            if status == "error":
                raise ArgumentNotValidException(arguments)

        except:
            if self.log:
                self._logging(f"major error occured with argument {arguments}")

            raise Exception(f"'{arguments}' resulted in an Error.")

    def activate(self):
        self.send_arguments(self._build_data(("on", "true")))

    def deactivate(self):
        self.send_arguments(self._build_data(("on", "false")))

    def toggle(self):
        self.send_arguments(self._build_data(("on", '"t"')))

    def set_brightness(self, brightness: int):
        if brightness < 0 or brightness > 255:
            raise ValueOutOfBoundsException(brightness)

        self.send_arguments(self._build_data(("bri", brightness)))

    def set_preset(self, preset: int):
        if preset < -1 or preset > 250:
            raise ValueOutOfBoundsException(preset)

        self.send_arguments(self._build_data(("ps", preset)))

    def set_primary_color(self, color: tuple[int, int, int]):
        if min(color) < 0 or max(color) > 255:
            raise ValueOutOfBoundsException(color, (0, 0, 0), (255, 255, 255))

        self.send_arguments(self._build_data(("col", '[' + str(list(color)) + ']')))

    def set_effect(self, effect: int):
        if effect < 0 or effect > 101:
            raise ValueOutOfBoundsException(effect, stop=101)

        self.send_arguments(self._build_data(("fx", effect)))

    def set_effect_speed(self, speed: int):
        if speed < 0 or speed > 255:
            raise ValueOutOfBoundsException(speed)

        self.send_arguments(self._build_data(("sx", speed)))

    def set_effect_intensity(self, intensity: int):
        if intensity < 0 or intensity > 255:
            raise ValueOutOfBoundsException(intensity)

        self.send_arguments(self._build_data(("ix", intensity)))

    def freeze(self):
        self.send_arguments(self._build_data(("frz", 'true')))

    def unfreeze(self):
        self.send_arguments(self._build_data(("frz", 'false')))
