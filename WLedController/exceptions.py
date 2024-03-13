class UnreachableSocketException(Exception):
    def __init__(self, socket: str):
        super().__init__(f"The Socket '{socket}' is not reachable.")


class ValueOutOfBoundsException(Exception):
    def __init__(self, value, start=0, stop=255):
        super().__init__(f"The Value '{value}' is out of the range ({start}, {stop}).")


class InvalidArgumentException(Exception):
    def __init__(self, argument: str):
        super().__init__(f"The argument '{argument}' is not valid.")


class InvalidMainKeyException(Exception):
    def __init__(self, main_key: str):
        super().__init__(f"The main key '{main_key}' is not valid.")
