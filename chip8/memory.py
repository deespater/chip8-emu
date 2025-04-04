from .errors import Chip8Panic
from .utils import parse_byte


class Chip8Memory:
    SIZE: int = 4 * 1024  # 4 kb

    data: bytearray

    def __init__(self) -> None:
        self.data = bytearray(self.SIZE)

    def _validate_address(self, address: int) -> None:
        if not 0 <= address < self.SIZE:
            raise Chip8Panic(f'Memory address out of bounds: {hex(address)}')

    def read_byte(self, address: int) -> int:
        self._validate_address(address)
        return self.data[address]

    def write_byte(self, address: int, byte: int) -> None:
        self._validate_address(address)
        self.data[address] = parse_byte(byte)

    def write(self, address: int, data: bytes | bytearray) -> None:
        # try:
        for byte in data:
            self.write_byte(address, byte)
            address += 1
        # except TypeError:
        #     import pudb; pudb.set_trace()

    def read(self, address: int, length: int) -> bytearray:
        buffer = bytearray(length)
        for i in range(length):
            buffer[i] = self.read_byte(address + i)
        return buffer
