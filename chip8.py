PROGRAM_START = 0x200 # ??

class Chip8Panic(Exception):
    pass

class Chip8Display:
    WIDTH: int = 64
    HEIGHT: int = 32

    memory: list[bytearray]

    def __init__(self):
        self.clear()

    def draw_sprite(self, sprite_data: bytes, sprite_x: int, sprite_y: int) -> None:
        """Setting sprite data to display memory"""

        for row_index, sprite_row_bytes in enumerate(sprite_data): # Length of sprite_data is the height of sprite so we iterating each row of sprite
            for column_index in range(8):  # Sprite is fixed 8 bit width
                dx = (sprite_x + column_index) % self.WIDTH  # Wrapping bits horizontally
                dy = (sprite_y + row_index) % self.HEIGHT  # Wrapping bits vertically

                sprite_pixel =  (sprite_row_bytes >> (7 - column_index)) & 1
                self.memory[dy][dx] = sprite_pixel

    def clear(self) -> None:
        """Clearing memory and setting it to 0"""
        self.memory = [bytearray(self.WIDTH) for _ in range(self.HEIGHT)]

    def render(self) -> None:
        """Rendering display memory to the screen"""
        print('\033[H', end='')  # ANSI clear screen
        for row in self.memory:
            print(''.join('▓' if pixel else ' ' for pixel in row))


class Chip8Registers:
    V_SIZE: int = 16

    V: bytearray
    I: int

    def __init__(self):
        self.V = bytearray(self.V_SIZE)
        self.I = 0

    def _validate_index(self, index: int) -> None:
        if index >= self.V_SIZE:
            raise Chip8Panic(f'Registry V: index "{hex(index)}" out of bounds')


    def setV(self, index: int, value: int) -> None:
        self._validate_index(index)
        self.V[index] = value

    def getV(self, index: int) -> int:
        self._validate_index(index)
        return self.V[index]

    def setI(self, value: int) -> None:
        self.I = value

    def getI(self) -> int:
        return self.I


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

class Chip8:
    PROGRAM_START: int = 0x200

    display: Chip8Display
    memory: Chip8Memory
    registers: Chip8Registers

    counter: int

    def __init__(self) -> None:
        self.display = Chip8Display()
        self.memory = Chip8Memory()
        self.registers = Chip8Registers()

        # Setting CPU counter to the 512th byte on boot
        self.counter = self.PROGRAM_START

    def fetch_opcode(self) -> int:
        # Since Chip8 uses 2 bytes opcodes, we are reading 2 bytes
        high_byte = self.memory.read_byte(self.counter)
        low_byte = self.memory.read_byte(self.counter + 1)

        # Returning one "16-bit" integer from two read bytes
        return (high_byte << 8) | low_byte

    def load_rom(self, path: str) -> None:
        # Load a CHIP-8 ROM file into memory starting at 0x200

        with open(path, 'rb') as rom_file:
            rom_data = rom_file.read()
            self.memory.write(self.PROGRAM_START, rom_data)

    def execute_opcode(self, opcode: int) -> None:
        nnn = opcode & 0x0FFF       # Addr: Lowest 12 bits of the opcode
        n = opcode & 0x000F         # Nibble: Lowest 4 bits of the opcode
        x = (opcode & 0x0F00) >> 8  # Register X: lower 4 bits of the high byte of the opcode
        y = (opcode & 0x00F0) >> 4  # Register Y: upper 4 bits of the high byte of the opcode
        kk = opcode & 0x00FF        # Immediate byte: the lowest 8 bits of the instruction


        # LIST OF IMPLEMENTED OPCODES
        # https://devernay.free.fr/hacks/chip8/C8TECH10.HTM#3.1
        match opcode:
            case 0x00E0:
                # 00E0 - CLS
                # Clear the display.
                self.display.clear()

            case _ if opcode & 0xF000 == 0x1000:
                # 1nnn - JP addr
                # Jump to location nnn.

                # The interpreter sets the program counter to nnn.
                self.counter = nnn

            case _ if opcode & 0xF000 == 0x6000:
                # 6xkk - LD Vx, byte
                # Set Vx = kk.

                # The interpreter puts the value kk into register Vx.
                self.registers.setV(x, kk)

            case _ if opcode & 0xF000 == 0x7000:
                # 7xkk - ADD Vx, byte
                # Set Vx = Vx + kk.

                # Adds the value kk to the value of register Vx, then stores the result in Vx.
                Vx = self.registers.getV(x)
                self.registers.setV(x, Vx + kk)

            case _ if opcode & 0xF000 == 0xA000:
                # Annn - LD I, addr
                # Set I = nnn.

                # The value of register I is set to nnn.
                self.registers.setI(nnn)

            case _ if opcode & 0xF000 == 0xD000:
                # Dxyn - DRW Vx, Vy, nibble
                # Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.

                # The interpreter reads n bytes from memory, starting at the address stored in I.
                # These bytes are then displayed as sprites on screen at coordinates (Vx, Vy).
                # Sprites are XORed onto the existing screen. If this causes any pixels to be erased, VF is set to 1,
                # otherwise it is set to 0. If the sprite is positioned so part of it is outside the coordinates of the display,
                # it wraps around to the opposite side of the screen.
                sprite_data = self.memory.read(self.registers.getI(), n)
                sprite_x = self.registers.getV(x)
                sprite_y = self.registers.getV(y)

                # Rendering the sprite
                self.display.draw_sprite(sprite_data, sprite_x, sprite_y)

            case _:
                raise Chip8Panic(f'Unknown opcode "{hex(opcode)}"')


    def tick(self) -> None:
        opcode = self.fetch_opcode()
        self.counter += 2

        self.execute_opcode(opcode)

        self.display.render()

    def run(self) -> None:
        while True:
            self.tick()
