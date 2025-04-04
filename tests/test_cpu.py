import pytest

from chip8.cpu import Chip8, Chip8Registers
from chip8.errors import Chip8Panic
from chip8.memory import Chip8Memory
from chip8.display import Chip8Display


@pytest.fixture
def chip8():
    """Fixture to create a Chip8 instance for testing."""
    return Chip8()

def test_chip8_initialization(chip8):
    assert chip8.counter == 0x200

    assert isinstance(chip8.display, Chip8Display)
    assert isinstance(chip8.memory, Chip8Memory)
    assert isinstance(chip8.registers, Chip8Registers)


def test_chip8_fetch_opcode(chip8):
    chip8.memory.write(0x200, bytes([0x12, 0x34]))
    opcode = chip8.fetch_opcode()

    assert opcode == 0x1234


### Opcode Tests ###
def test_chip8_execute_opcode_00E0(chip8, mocker):
    mocker.patch.object(chip8.display, 'clear')
    chip8.execute_opcode(0x00E0)

    # Check if the display clear method was called
    assert chip8.display.clear.called

def test_chip8_execute_opcode_1nnn(chip8):
    chip8.execute_opcode(0x1234)
    assert chip8.counter == 0x234


def test_chip8_execute_opcode_6xkk(chip8):
    chip8.execute_opcode(0x60FF)  # Set V0 = 0xFF
    assert chip8.registers.get_v(0) == 0xFF

    chip8.execute_opcode(0x61AA)  # Set V1 = 0xAA
    assert chip8.registers.get_v(1) == 0xAA

    # Verifying that registers are not affected by other opcodes
    assert chip8.registers.get_v(0) == 0xFF


def test_chip8_execute_opcode_7xkk(chip8):
    chip8.registers.set_v(1, 0x01)
    chip8.execute_opcode(0x7111)  # Add 0x11 to V1

    assert chip8.registers.get_v(1) == 0x12


def test_chip8_execute_opcode_Annn(chip8):
    chip8.execute_opcode(0xA123)  # Set I = 0x123
    assert chip8.registers.get_i() == 0x123


def test_chip8_execute_opcode_Dxyn(chip8, mocker):
    mocker.patch.object(chip8.display, 'draw_sprite')

    sprite_offset = 0x300
    sprite_data = bytes([0b11110011, 0b00001100])
    sprite_x = 0x04
    sprite_y = 0x04

    chip8.registers.set_i(sprite_offset)
    chip8.memory.write(sprite_offset, sprite_data)
    chip8.registers.set_v(2, sprite_x)
    chip8.registers.set_v(3, sprite_y)

    chip8.execute_opcode(0xD232)  # Draw sprite at (V2, V3) with height 2

    # Check if the display draw_sprite method was called with the correct parameters
    assert chip8.display.draw_sprite.called
    args, _ = chip8.display.draw_sprite.call_args
    assert args[0] == sprite_data
    assert args[1] == sprite_x
    assert args[2] == sprite_y


def test_chip8_execute_opcode_unknown(chip8):
    with pytest.raises(Chip8Panic, match='Unknown opcode "0xffff"'):
        chip8.execute_opcode(0xFFFF)


def test_chip8_tick(chip8, mocker):
    mocker.patch.object(chip8, 'fetch_opcode', return_value=0x00E0)
    mocker.patch.object(chip8, 'execute_opcode')
    mocker.patch.object(chip8.display, 'render')

    chip8.tick()

    assert chip8.counter == chip8.PROGRAM_START + 2
    assert chip8.execute_opcode.called
    assert chip8.display.render.called
