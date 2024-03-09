class UnreachableAddressException(Exception):
    def __init__(self, ip_address: str):
        super().__init__(f"The IP-Address '{ip_address}' is not reachable.")


class ValueOutOfBoundsException(Exception):
    def __init__(self, value, start=0, stop=255):
        super().__init__(f"The Value '{value}' is out of the range ({start}, {stop}).")


class ArgumentNotValidException(Exception):
    def __init__(self, argument: str):
        super().__init__(f"The argument '{argument}' is not valid.")
