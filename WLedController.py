import json
import math
from datetime import datetime
from enum import Enum

import requests.exceptions

import exceptions


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
        self._log = log

        try:
            self.get_status()
        except:
            raise exceptions.UnreachableSocketException(wled_socket)

    # private assisting methods
    @staticmethod
    def _get_request(request: str) -> requests.models.Response:
        return requests.get(request)

    @staticmethod
    def _post_request(request: str, arguments: str) -> requests.models.Response:
        return requests.post(request, arguments)

    @staticmethod
    def _timestamp() -> str:
        return str(datetime.now())[:-7]

    @staticmethod
    def _build_data(*args: tuple[str: any]):
        return "{" + ", ".join([f'"{arg[0]}": {arg[1]}' for arg in args]) + "}"

    def _logging(self, msg: str):
        print(f"{self._timestamp()}: {msg}")

    # config settings
    def activate_log(self) -> None:
        self._log = True

    def deactivate_log(self) -> None:
        self._log = False

    # get requests
    def get_version(self) -> int:
        return int(self._get_request(self.api_url + "version").text)

    def get_free_heap(self) -> int:
        return int(self._get_request(self.api_url + "freeheap").text)

    def get_uptime(self) -> int:
        return int(self._get_request(self.api_url + "uptime").text)

    def get_timer(self) -> int:
        return self.get_status(Specifier.state, "nl")["rem"]

    def get_status(self, specification: Specifier = Specifier.none, main_key: str = None) -> dict[str: dict[str: any]]:
        response = self._get_request(self.json_url + specification.value).json()
        if main_key:
            try:
                return response[main_key]
            except KeyError:
                raise exceptions.InvalidMainKeyException(main_key)
        else:
            return response

    # nonparametric functions
    def reboot(self) -> int:
        return self._get_request(self.api_url + "reset").status_code

    def activate(self) -> None:
        self.set_arguments(self._build_data(("on", "true")))

    def deactivate(self) -> None:
        self.set_arguments(self._build_data(("on", "false")))

    def toggle(self) -> None:
        self.set_arguments(self._build_data(("on", '"t"')))

    def activate_timer(self) -> None:
        self.set_arguments(self._build_data(("nl.on", 'true')))

    def deactivate_timer(self) -> None:
        self.set_arguments(self._build_data(("nl.on", 'false')))

    def activate_live(self) -> None:
        self.set_arguments(self._build_data(("live", 'true')))

    def deactivate_live(self) -> None:
        self.set_arguments(self._build_data(("live", 'false')))

    # parametric functions
    def set_arguments(self, arguments: str) -> None:
        try:
            status = list(json.loads(self._post_request(self.json_url, arguments).text))[0]

            if self._log:
                self._logging(f"{arguments} --> {status}")

            if status == "error":
                raise exceptions.InvalidArgumentException(arguments)

        except:
            if self._log:
                self._logging(f"major error occured with argument {arguments}")

            raise Exception(f"'{arguments}' resulted in an Error.")

    def set_brightness(self, brightness: int) -> None:
        if brightness < 0 or brightness > 255:
            raise exceptions.ValueOutOfBoundsException(brightness)

        self.set_arguments(self._build_data(("bri", brightness)))

    def set_transition(self, milliseconds: int) -> None:
        milliseconds = milliseconds / 100

        if milliseconds < 0 or milliseconds > 65535:
            raise exceptions.ValueOutOfBoundsException(milliseconds, stop=65535)

        self.set_arguments(self._build_data(("transition", math.floor(milliseconds))))

    def set_preset(self, preset: int) -> None:
        if preset < -1 or preset > 250:
            raise exceptions.ValueOutOfBoundsException(preset, start=-1, stop=250)

        self.set_arguments(self._build_data(("ps", preset)))

    def set_timer(self, minutes: int) -> None:
        if minutes < 0 or minutes > 255:
            raise exceptions.ValueOutOfBoundsException(minutes)

        self.set_arguments(self._build_data(("nl.dur", minutes)))

    def set_timer_mode(self, mode: NightlightMode) -> None:
        self.set_arguments(self._build_data(("nl.mode", mode.value)))

    def set_timer_brightness(self, target_brightness: int) -> None:
        if target_brightness < 0 or target_brightness > 255:
            raise exceptions.ValueOutOfBoundsException(target_brightness)

        self.set_arguments(self._build_data(("nl.tbri", target_brightness)))

    def set_colors(self, *colors: list[int, int, int]) -> None:
        for color in colors:
            if min(color) < 0 or max(color) > 255:
                raise exceptions.ValueOutOfBoundsException(color, (0, 0, 0), (255, 255, 255))

        self.set_arguments(self._build_data(("seg", self._build_data(("col", str(list(colors)))))))

    def set_effect(self, effect: int) -> None:
        if effect < 0 or effect > 117:
            raise exceptions.ValueOutOfBoundsException(effect, stop=101)

        self.set_arguments(self._build_data(("seg", self._build_data(("fx", effect)))))

    def set_effect_speed(self, speed: int) -> None:
        if speed < 0 or speed > 255:
            raise exceptions.ValueOutOfBoundsException(speed)

        self.set_arguments(self._build_data(("seg", self._build_data(("sx", speed)))))

    def set_effect_intensity(self, intensity: int) -> None:
        if intensity < 0 or intensity > 255:
            raise exceptions.ValueOutOfBoundsException(intensity)

        self.set_arguments(self._build_data(("seg", self._build_data(("ix", intensity)))))
