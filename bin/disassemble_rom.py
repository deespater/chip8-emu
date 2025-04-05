from pathlib import Path


def get_opcode_name(opcode: int) -> str:
    nnn = opcode & 0x0FFF       # Addr: Lowest 12 bits of the opcode
    n = opcode & 0x000F         # Nibble: Lowest 4 bits of the opcode
    x = (opcode & 0x0F00) >> 8       # Register X: lower 4 bits of the high byte
    y = (opcode & 0x00F0) >> 4       # Register Y: upper 4 bits of the high byte
    kk = opcode & 0x00FF        # Immediate byte: the lowest 8 bits

    match opcode:
        case 0x00E0:
            return '00E0 - CLS'
        case _ if opcode & 0xF000 == 0x1000:
            return f'1nnn - JP {nnn:04x}'
        case _ if opcode & 0xF000 == 0x3000:
            return f'3xkk - SE V{x}, {kk}'
        case _ if opcode & 0xF000 == 0x4000:
            return f'4xkk - SNE V{x}, {kk}'
        case _ if opcode & 0xF000 == 0x6000:
            return f'6xkk - LD V{x}, {kk}'
        case _ if opcode & 0xF000 == 0x7000:
            return f'7xkk - ADD V{x}, {kk}'
        case _ if opcode & 0xF00F == 0x8004:
            return f'8xy4 - ADD V{x}, V{y}'
        case _ if opcode & 0xF000 == 0xA000:
            return f'Annn - LD I, {nnn}'
        case _ if opcode & 0xF000 == 0xD000:
            return f'Dxyn - DRW V{x}, V{y}, {n}'
        case _ if opcode & 0xF0FF == 0xF007:
            return f'Fx07 - LD V{x}, DT'
        case _ if opcode & 0xF0FF == 0xF00A:
            return f'Fx0A - LD V{x}, K'
        case _ if opcode & 0xF0FF == 0xF015:
            return f'Fx15 - LD DT, V{x}'
        case _ if opcode & 0xF0FF == 0xF018:
            return f'Fx18 - LD ST, V{x}'
        case _:
            return f'Unknown opcode: "{hex(opcode)}"'


def read_opcode(opcode: int) -> str:
    """
    Read opcode and return its string representation.
    """
    # Convert the opcode to a 4-digit hexadecimal string
    hex_opcode = f'{opcode:04X}'

    # # Split the opcode into its components
    nibbles = [ hex_opcode[i : i + 2] for i in range(0, len(hex_opcode), 2) ]

    # Format the opcode as a string
    return '0x' + ' '.join(nibbles)


if __name__ == '__main__':
    rom_data = Path('./demo.bin').read_bytes()

    for i in range(0, len(rom_data), 2):
        # Read two bytes from the ROM data
        opcode = (rom_data[i] << 8) | rom_data[i + 1]

        opcode_name = get_opcode_name(opcode)

        print(f'{i + 0x200:04x}: {opcode:04x} — {opcode_name}')
