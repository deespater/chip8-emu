import pytest

from chip8.errors import Chip8Panic
from chip8.utils import parse_byte


@pytest.mark.parametrize(('value', 'length', 'expected_msg'), [
    (0, 1, 0),
    (255, 1, 255),
    (16, 2, 16),
    (65535, 2, 65535),
    (256, 1, '256 is not valid for 1 byte'),
    (65536, 2, '65536 is not valid for 2 byte'),
    (16777216, 3, '16777216 is not valid for 3 byte'),
])
def test_parse_byte(value, length, expected_msg):
    if isinstance(expected_msg, int):
        assert parse_byte(value, length) == expected_msg
        return

    # If expected_msg is a string, we expect an exception
    with pytest.raises(Chip8Panic, match=expected_msg):
        parse_byte(value, length)
