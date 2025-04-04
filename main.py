from chip8 import Chip8

if __name__ == '__main__':
    chip = Chip8()
    chip.load_rom('./IBM Logo.ch8')  # Replace with your ROM path

    try:
        chip.run()
    except KeyboardInterrupt:
        print('\nStopped')
