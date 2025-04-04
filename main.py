import os

from chip8 import Chip8


def clear_screen() -> None:
    os.system('clear')  # noqa: S605, S607


if __name__ == '__main__':
    # Clear terminal on start
    clear_screen()

    chip = Chip8()
    chip.load_rom('./IBM Logo.ch8')  # Replace with your ROM path

    try:
        chip.run()
    except KeyboardInterrupt:
        clear_screen()
        print('\nStopped')
