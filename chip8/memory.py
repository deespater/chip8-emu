from .errors import Chip8Panic
from .utils import parse_byte


class Chip8Memory:
    SIZE: int = 4 * 1024  # 4 kb

    data: bytearray

    def __init__(self) -> None:
        self.data = bytearray(self.SIZE)

    def read_byte(self, address: int) -> int:
        if not 0 <= address < self.SIZE:
            raise Chip8Panic(f'Memory read out of bounds: {hex(address)}')

        return self.data[address]

    def write_byte(self, address: int, byte: int) -> None:
        if not 0 <= address < self.SIZE:
            raise Chip8Panic(f'Memory write out of bounds: {hex(address)}')

        self.data[address] = parse_byte(byte)

    def write(self, address: int, data: bytes | bytearray) -> None:
        if not 0 <= address + len(data) < self.SIZE:
            raise Chip8Panic(f'Memory write out of bounds: {hex(self.SIZE)}')

        self.data[address:address + len(data)] = data

    def read(self, address: int, length: int) -> bytearray:
        if not 0 <= address + length < self.SIZE:
            raise Chip8Panic(f'Memory read out of bounds: {hex(self.SIZE)}')

        buffer = bytearray(length)
        for i in range(length):
            buffer[i] = self.read_byte(address + i)
        return buffer
