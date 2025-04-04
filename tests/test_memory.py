import pytest

from chip8.errors import Chip8Panic
from chip8.memory import Chip8Memory


def test_memory_initialization():
    memory = Chip8Memory()
    assert len(memory.data) == Chip8Memory.SIZE
    assert all(byte == 0 for byte in memory.data)


def test_read_byte_within_bounds():
    memory = Chip8Memory()
    memory.data[0x100] = 0xAB
    assert memory.read_byte(0x100) == 0xAB


def test_read_byte_out_of_bounds():
    memory = Chip8Memory()
    with pytest.raises(Chip8Panic, match='Memory read out of bounds: 0x1000'):
        memory.read_byte(0x1000)


def test_write_byte_within_bounds():
    memory = Chip8Memory()
    memory.write_byte(0x200, 0xCD)
    assert memory.data[0x200] == 0xCD


def test_write_byte_out_of_bounds():
    memory = Chip8Memory()
    with pytest.raises(Chip8Panic, match='Memory write out of bounds: 0x1000'):
        memory.write_byte(0x1000, 0xEF)


def test_write_byte_invalid_value():
    memory = Chip8Memory()
    with pytest.raises(Chip8Panic, match='Value 300 is not a valid byte'):
        memory.write_byte(0x200, 300)


def test_write_within_bounds():
    memory = Chip8Memory()
    data = bytes([0x01, 0x02, 0x03])
    memory.write(0x300, data)
    assert memory.data[0x300:0x303] == data


def test_write_out_of_bounds():
    memory = Chip8Memory()
    data = bytes([0x01, 0x02, 0x03])

    error_msg = 'Memory write data outside memory bounds'
    with pytest.raises(Chip8Panic, match=error_msg):
        memory.write(0xFFF, data)


def test_read_within_bounds():
    memory = Chip8Memory()
    memory.data[0x400:0x403] = bytes([0x04, 0x05, 0x06])
    result = memory.read(0x400, 3)
    assert result == bytearray([0x04, 0x05, 0x06])


def test_read_out_of_bounds():
    memory = Chip8Memory()

    error_msg = 'Memory read out of bounds: 0xfff'
    with pytest.raises(Chip8Panic, match=error_msg):
        memory.read(0xFFF, 3)
