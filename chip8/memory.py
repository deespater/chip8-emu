from .errors import Chip8Panic


class Chip8Memory:
    SIZE: int = 4 * 1024  # 4 kb

    data: bytearray

    def __init__(self) -> None:
        self.data = bytearray(self.SIZE)

    def read_byte(self, address: int) -> int:
        if not 0 <= address < len(self.data):
            raise Chip8Panic(f'Memory read out of bounds: {hex(address)}')

        return self.data[address]

    def write_byte(self, address: int, value: int) -> None:
        if not 0 <= address < len(self.data):
            raise Chip8Panic(f'Memory write out of bounds: {hex(address)}')

        if not 0 <= value <= 0xFF:
            raise Chip8Panic(f'Value {value} is not a valid byte (0-255)')

        self.data[address] = value

    def write(self, address: int, data: bytes | bytearray) -> None:
        if not 0 <= address <= len(self.data) - len(data):
            raise Chip8Panic('Memory write data outside memory bounds')

        self.data[address:address + len(data)] = data

    def read(self, address: int, length: int) -> bytearray:
        if not 0 <= address <= len(self.data) - length:
            raise Chip8Panic(f'Memory read out of bounds: {hex(address)} with length: {length}')

        return bytearray(self.data[address:address + length])
