import json
from datetime import datetime
from enum import Enum

import requests.exceptions

from exceptions import *


class Specifier(Enum):
    none = ""
    state = "state"
    info = "info"
    effects = "effects"
    palettes = "palettes"
    live = "live"


class NightlightMode(Enum):
    instant = 0
    fade = 1
    color_fade = 2
    sunrise = 3


class WLedController:
    def __init__(self, wled_socket: str, log: bool = True) -> None:
        self.api_url = f"http://{wled_socket}/"
        self.json_url = self.api_url + "json/"
        self.log = log

        try:
            self.get_status()
        except:
            raise UnreachableSocketException(wled_socket)

    @staticmethod
    def _get_request(request: str):
        return requests.get(request, proxies={'http': "http://localhost:3128"})

    @staticmethod
    def _post_request(request: str, arguments: str):
        return requests.post(request, arguments, proxies={'http': "http://localhost:3128"})

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

    def get_version(self):
        print(self.json_url + "version")
        return self._get_request(self.json_url + "version").text

    def get_free_heap(self):
        return self._get_request(self.json_url + "freeheap").text

    def get_status(self, specification: Specifier = Specifier.none, main_key: str = None) -> dict:
        response = self._get_request(self.json_url + specification.value).json()
        if main_key:
            try:
                return response[main_key]
            except KeyError:
                raise InvalidMainKeyException(main_key)
        else:
            return response

    def get_timer(self):
        return self.get_status(Specifier.state, "nl")["rem"]

    def reboot(self):
        self.set_arguments(self._build_data(("rb", "true")))

    def activate(self):
        self.set_arguments(self._build_data(("on", "true")))

    def deactivate(self):
        self.set_arguments(self._build_data(("on", "false")))

    def toggle(self):
        self.set_arguments(self._build_data(("on", '"t"')))

    def activate_timer(self):
        self.set_arguments(self._build_data(("nl.on", 'true')))

    def deactivate_timer(self):
        self.set_arguments(self._build_data(("nl.on", 'false')))

    def activate_live(self):
        self.set_arguments(self._build_data(("live", 'true')))

    def deactivate_live(self):
        self.set_arguments(self._build_data(("live", 'false')))

    def set_arguments(self, arguments: str):
        try:
            status = list(json.loads(self._post_request(self.json_url, arguments).text))[0]

            if self.log:
                self._logging(f"{arguments} --> {status}")

            if status == "error":
                raise InvalidArgumentException(arguments)

        except:
            if self.log:
                self._logging(f"major error occured with argument {arguments}")

            raise Exception(f"'{arguments}' resulted in an Error.")

    def set_brightness(self, brightness: int):
        if brightness < 0 or brightness > 255:
            raise ValueOutOfBoundsException(brightness)

        self.set_arguments(self._build_data(("bri", brightness)))

    def set_transition(self, milliseconds: int):
        milliseconds = milliseconds // 100

        if milliseconds < 0 or milliseconds > 65535:
            raise ValueOutOfBoundsException(milliseconds)

        self.set_arguments(self._build_data(("transition", milliseconds)))

    def set_preset(self, preset: int):
        if preset < -1 or preset > 250:
            raise ValueOutOfBoundsException(preset)

        self.set_arguments(self._build_data(("ps", preset)))

    def set_timer(self, minutes: int):
        if minutes < 0 or minutes > 255:
            raise ValueOutOfBoundsException(minutes)

        self.set_arguments(self._build_data(("nl.dur", minutes)))

    def set_timer_mode(self, mode: NightlightMode):
        self.set_arguments(self._build_data(("nl.mode", mode.value)))

    def set_timer_brightness(self, target_brightness: int):
        if target_brightness < 0 or target_brightness > 255:
            raise ValueOutOfBoundsException(target_brightness)

        self.set_arguments(self._build_data(("nl.tbri", target_brightness)))

    def set_primary_color(self, color: tuple[int, int, int]):
        if min(color) < 0 or max(color) > 255:
            raise ValueOutOfBoundsException(color, (0, 0, 0), (255, 255, 255))

        self.set_arguments(self._build_data(("col", '[' + str(list(color)) + ']')))

    def set_effect(self, effect: int):
        if effect < 0 or effect > 101:
            raise ValueOutOfBoundsException(effect, stop=101)

        self.set_arguments(self._build_data(("fx", effect)))

    def set_effect_speed(self, speed: int):
        if speed < 0 or speed > 255:
            raise ValueOutOfBoundsException(speed)

        self.set_arguments(self._build_data(("sx", speed)))

    def set_effect_intensity(self, intensity: int):
        if intensity < 0 or intensity > 255:
            raise ValueOutOfBoundsException(intensity)

        self.set_arguments(self._build_data(("ix", intensity)))

    def freeze(self):
        self.set_arguments(self._build_data(("frz", 'true')))

    def unfreeze(self):
        self.set_arguments(self._build_data(("frz", 'false')))


wled = WLedController("130.185.38.241:8080")
print(wled.get_version())
print(wled.get_free_heap())
wled.deactivate()

# url
# reset
# uptime
# print(requests.get("http://130.185.38.241:8080/freeheap", proxies={'http': "http://localhost:3128"}).json())
