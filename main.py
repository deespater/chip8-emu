from chip8 import Chip8

if __name__ == '__main__':
    import os

    os.system('clear')  # Clear terminal on start

    chip = Chip8()
    # chip.load_rom("your_test.rom")  # Replace with your ROM path

    try:
        chip.run()
    except KeyboardInterrupt:
        print("\nStopped.")
