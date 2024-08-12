from typing import Any


_resistance = 100.


def get_resistance() -> float:
    global _resistance
    return _resistance


def set_resistance(value: float) -> None:
    global _resistance
    _resistance = value


class Device:

    def __init__(self, com_port: str) -> None:
        self.com_port = com_port
        self.cs = False
        self.vm = False
        self.current = 0.
        self.auto_range = True
        self.max_voltage = 10.

    def set(self, identifier: str, name: str, value: Any) -> None:
        if name in ['ENABLE', 'DISABLE']:
            if identifier == 'CS':
                self.cs = name == 'ENABLE'
            elif identifier == 'VM':
                self.vm = name == 'ENABLE'
        elif identifier != 'CS':
            return
        elif name == 'SOURCE':
            voltage = get_resistance() * value
            self.current = value if voltage <= self.max_voltage else 0.
        elif name == 'AR':
            self.auto_range = value
        elif name == 'MV':
            self.max_voltage = value

    def get(self, identifier: str, name: str) -> Any:
        if name == 'MEASURE':
            if identifier == 'CS' and self.cs:
                return self.current
            if identifier == 'VM' and self.vm:
                voltage = get_resistance() * self.current
                return voltage
        elif identifier != 'CS':
            return
        elif name == 'AR':
            return self.auto_range
        elif name == 'MV':
            return self.max_voltage


class Interface:

    def __init__(self, com_port: str) -> None:
        self.com_port = com_port

    @staticmethod
    def select(new_contact: str) -> None:
        for contact_id, new_resistance in zip(['BL', 'BR', 'TL', 'TR'], [100., 200., 50., 1000.]):
            if contact_id == new_contact:
                set_resistance(new_resistance)
