from datetime import datetime
from time import sleep

import requests.exceptions

from exceptions import *


class WLedController:
    def __init__(self, wled_ip_address: str) -> None:
        self.api_url = f"http://{wled_ip_address}/win"
        self.log = True

        try:
            self.get_status()
        except:
            raise UnreachableAddressException(wled_ip_address)

    @staticmethod
    def _timestamp() -> str:
        return str(datetime.now())[:-7]

    def activate_log(self):
        self.log = True

    def deactivate_log(self):
        self.log = False

    def send_arguments(self, *args):
        statement = self.api_url + "&" + "&".join(args)

        try:
            requests.put(statement)

            if self.log:
                print(statement, flush=True)

        except:
            raise Exception(f"'{statement}' could not be executed.")

    def activate(self):
        self.send_arguments("T=1")

    def deactivate(self):
        self.send_arguments("T=0")

    def get_status(self) -> str:
        return requests.get(self.api_url).text

    def set_preset(self, preset: int):
        if preset < 0 or preset > 255:
            raise ValueOutOfBoundsException(preset)

        self.send_arguments(f"PL={preset}")

    def set_color(self, color: tuple[int, int, int]):
        if min(color) < 0 or max(color) > 255:
            raise ValueOutOfBoundsException(color, (0, 0, 0), (255, 255, 255))

        self.send_arguments(f"R={color[0]}", f"G={color[1]}", f"B={color[2]}")

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
