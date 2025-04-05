import os
import argparse
from pathlib import Path

from chip8 import Chip8


def clear_screen() -> None:
    os.system('clear')  # noqa: S605, S607


if __name__ == '__main__':
    chip = Chip8()

    parser = argparse.ArgumentParser(description='Run the CHIP-8 emulator.')
    parser.add_argument('rom_path', type=str, help='Path to the ROM file to load.')
    args = parser.parse_args()

    rom_data = Path(args.rom_path).read_bytes()
    chip.memory.write(chip.PROGRAM_START, rom_data)

    try:
        # clear_screen()
        chip.run()
    except KeyboardInterrupt:
        # clear_screen()
        print('\nStopped')
