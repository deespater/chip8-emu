import os
from pathlib import Path

from chip8 import Chip8


def clear_screen() -> None:
    os.system('clear')  # noqa: S605, S607


if __name__ == '__main__':
    chip = Chip8()

    rom_data = Path('./dummy.bin').read_bytes()
    chip.memory.write(chip.PROGRAM_START, rom_data)

    try:
        clear_screen()
        chip.run()
    except KeyboardInterrupt:
        clear_screen()
        print('\nStopped')
