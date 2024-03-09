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

    def set_color(self, color: tuple[int, int, int]):
        if min(color) < 0 or max(color) > 255:
            raise ValueOutOfBoundsException(color, (0, 0, 0), (255, 255, 255))

        self.send_arguments(self._build_data(("col", '['+str(list(color))+']')))

    def set_effect(self, effect: int):
        if effect < 0 or effect > 101:
            raise ValueOutOfBoundsException(effect, stop=101)

        self.send_arguments(f"FX={effect}")

    def set_effect_speed(self, speed: int):
        if speed < 0 or speed > 255:
            raise ValueOutOfBoundsException(speed)

        self.send_arguments(f"SX={speed}")

    def set_effect_intensity(self, intensity: int):
        if intensity < 0 or intensity > 255:
            raise ValueOutOfBoundsException(intensity)

        self.send_arguments(f"IX={intensity}")

    def set_palette(self, palette: int):
        if palette < 0 or palette > 255:
            raise ValueOutOfBoundsException(palette)

        self.send_arguments(f"FP={palette}")

    def stop_timer(self):
        self.deactivate()
        sleep(.1)
        self.activate()

    def set_timer(self, target_brightness: int = 0, timer: int = None):
        if timer and (min(target_brightness, timer) < 0 or max(target_brightness, timer) > 255):
            raise ValueOutOfBoundsException(timer)

        if not timer:
            self.send_arguments("ND", f"NT={target_brightness}")
        else:
            self.send_arguments(f"NL={timer}", f"NT={target_brightness}")

    def hour_marker(self, timeout: int):
        last_marker = datetime.now().hour

        while True:
            now = datetime.now()
            not_off = "<ac>0</ac>" not in self.get_status()
            unmarked_new_hour = now.minute == 0 and now.hour != last_marker

            if not_off and unmarked_new_hour:
                timestamp = str(now)[:-7]
                print(f"{timestamp}: hour marked", flush=True)

                last_marker = now.hour

                iteration_range = now.hour % 12 - 1
                if iteration_range < 0:
                    iteration_range = 12

                self.send_arguments("PS=255")
                self.set_preset(1)
                sleep(1)
                for _ in range(iteration_range):
                    self.send_arguments("A=16")
                    sleep(1)
                    self.set_preset(1)
                    sleep(1)

                self.set_preset(255)

            sleep(timeout)


print(WLedController("192.168.178.42").set_color((25, 25, 25)))
