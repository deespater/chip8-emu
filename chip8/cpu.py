from .display import Chip8Display
from .errors import Chip8Panic
from .memory import Chip8Memory
from .timers import DelayTimer, SoundTimer
from .utils import parse_byte


class Chip8Registers:
    V_SIZE: int = 16  # Amount of 8-bit registers (V0 to VF)

    v: bytearray  # 16 x 8-bit data register: V0 to VF
    i: int  # 16 bit address register noqa: E741

    def __init__(self) -> None:
        self.v = bytearray(self.V_SIZE)
        self.i = 0

    def _validate_v_index(self, index: int) -> None:
        if not 0 <= index < self.V_SIZE:
            raise Chip8Panic(f'V register index out of bounds: {index}')

    def set_v(self, index: int, value: int) -> None:
        self._validate_v_index(index)
        self.v[index] = parse_byte(value)

    def get_v(self, index: int) -> int:
        self._validate_v_index(index)
        return self.v[index]

    def set_i(self, value: int) -> None:
        self.i = parse_byte(value, length=2)

    def get_i(self) -> int:
        return self.i


class Chip8:
    FREQUENCY: int = 60  # Hz

    PROGRAM_START: int = 0x200

    display: Chip8Display
    memory: Chip8Memory
    registers: Chip8Registers

    delay_timer: DelayTimer
    sound_timer: SoundTimer

    counter: int

    def __init__(self) -> None:
        self.display = Chip8Display()
        self.memory = Chip8Memory()
        self.registers = Chip8Registers()

        self.delay_timer = DelayTimer()
        self.sound_timer = SoundTimer()

        # Setting CPU counter to the 512th byte on boot
        self.counter = self.PROGRAM_START

    def fetch_opcode(self) -> int:
        # Since Chip8 uses 2 bytes opcodes, we are reading 2 bytes
        [ high_byte, low_byte ] = self.memory.read(self.counter, 2)

        # Returning one "16-bit" integer from two read bytes
        return (high_byte << 8) | low_byte

    def execute_opcode(self, opcode: int) -> None:
        nnn = opcode & 0x0FFF       # Addr: Lowest 12 bits of the opcode
        n = opcode & 0x000F         # Nibble: Lowest 4 bits of the opcode
        x = (opcode & 0x0F00) >> 8  # Register X: lower 4 bits of the high byte
        y = (opcode & 0x00F0) >> 4  # Register Y: upper 4 bits of the high byte
        kk = opcode & 0x00FF        # Immediate byte: the lowest 8 bits

        # LIST OF IMPLEMENTED OPCODES
        # https://devernay.free.fr/hacks/chip8/C8TECH10.HTM#3.1
        match opcode:
            case 0x00E0:
                # 00E0 - CLS
                # Clear the display.
                self.display.clear()

            case _ if opcode & 0xF000 == 0x1000:  # noqa: PLR2004
                # 1nnn - JP addr
                # Jump to location nnn.

                # The interpreter sets the program counter to nnn.
                self.counter = nnn

            case _ if opcode & 0xF000 == 0x6000:  # noqa: PLR2004
                # 6xkk - LD Vx, byte
                # Set Vx = kk.

                # The interpreter puts the value kk into register Vx.
                self.registers.set_v(x, kk)

            case _ if opcode & 0xF000 == 0x7000:  # noqa: PLR2004
                # 7xkk - ADD Vx, byte
                # Set Vx = Vx + kk.

                # Adds the value kk to the value of register Vx,
                # then stores the result in Vx.
                vx = self.registers.get_v(x)
                self.registers.set_v(x, vx + kk)

            case _ if opcode & 0xF000 == 0xA000:  # noqa: PLR2004
                # Annn - LD I, addr
                # Set I = nnn.

                # The value of register I is set to nnn.
                self.registers.set_i(nnn)

            case _ if opcode & 0xF000 == 0xD000:  # noqa: PLR2004
                # Dxyn - DRW Vx, Vy, nibble
                # Display n-byte sprite from memory location I at (Vx, Vy),
                # set VF = collision.

                # The interpreter reads n bytes from memory, starting at the
                # address stored in I.These bytes are then displayed as sprites
                # on screen at coordinates (Vx, Vy). Sprites are XORed onto
                # the existing screen. If this causes any pixels to be erased,
                # VF is set to 1, otherwise it is set to 0. If the sprite is
                # positioned so part of it is outside the coordinates of the
                # display, it wraps around to the opposite side of the screen.
                sprite_data = self.memory.read(self.registers.get_i(), n)
                sprite_x = self.registers.get_v(x)
                sprite_y = self.registers.get_v(y)

                # Rendering the sprite
                self.display.draw_sprite(sprite_data, sprite_x, sprite_y)

            case _ if opcode & 0xF0FF == 0xF007:  # noqa: PLR2004
                # Fx07 - LD Vx, DT
                # Set Vx = delay timer value.

                # The value of DT is placed into Vx.
                self.registers.set_v(x, self.delay_timer.value)

            case _ if opcode & 0xF0FF == 0xF015:  # noqa: PLR2004
                # Fx15 - LD DT, Vx
                # Set delay timer = Vx.

                # DT is set equal to the value of Vx.
                self.delay_timer.update(self.registers.get_v(x))

            case _ if opcode & 0xF0FF == 0xF018:  # noqa: PLR2004
                # Fx18 - LD ST, Vx
                # Set sound timer = Vx.

                # ST is set equal to the value of Vx.
                self.sound_timer.update(self.registers.get_v(x))

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
