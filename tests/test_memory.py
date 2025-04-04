import pytest

from chip8.errors import Chip8Panic
from chip8.memory import Chip8Memory


@pytest.fixture
def chip8_memory():
    """Fixture to create a Chip8Memory instance for testing."""
    return Chip8Memory()


def test_memory_initialization(chip8_memory):
    assert len(chip8_memory.data) == Chip8Memory.SIZE
    assert all(byte == 0 for byte in chip8_memory.data)


def test_read_byte_within_bounds(chip8_memory):
    chip8_memory.data[0x100] = 0xAB
    assert chip8_memory.read_byte(0x100) == 0xAB


def test_read_byte_out_of_bounds(chip8_memory):
    error_msg = 'Memory read out of bounds: 0x2000'
    with pytest.raises(Chip8Panic, match=error_msg):
        chip8_memory.read_byte(0x2000)


def test_write_byte_within_bounds(chip8_memory):
    chip8_memory.write_byte(0x200, 0xCD)
    assert chip8_memory.data[0x200] == 0xCD


def test_write_byte_out_of_bounds(chip8_memory):
    error_msg = 'Memory write out of bounds: 0x1000'
    with pytest.raises(Chip8Panic, match=error_msg):
        chip8_memory.write_byte(0x1000, 0xEF)


def test_write_byte_invalid_value(chip8_memory):
    error_msg = '300 is not valid for 1 byte'
    with pytest.raises(Chip8Panic, match=error_msg):
        chip8_memory.write_byte(0x200, 300)


def test_write_within_bounds(chip8_memory):
    data = bytes([0x01, 0x02, 0x03])
    chip8_memory.write(0x300, data)
    assert chip8_memory.data[0x300:0x303] == data


def test_write_out_of_bounds(chip8_memory):
    data = bytes([0x01, 0x02, 0x03])

    error_msg = 'Memory write out of bounds: 0x1000'
    with pytest.raises(Chip8Panic, match=error_msg):
        chip8_memory.write(0xFFF, data)


def test_read_within_bounds(chip8_memory):
    chip8_memory.data[0x400:0x403] = bytes([0x04, 0x05, 0x06])
    result = chip8_memory.read(0x400, 3)
    assert result == bytearray([0x04, 0x05, 0x06])


def test_read_out_of_bounds(chip8_memory):
    error_msg = 'Memory read out of bounds: 0x1000'
    with pytest.raises(Chip8Panic, match=error_msg):
        chip8_memory.read(0xFFF, 3)
