from .errors import Chip8Panic


def parse_byte(value: int, length: int = 1) -> int:
    # Max value based on length: 1 byte = 0...255, 2 bytes = 0..65535
    max_value = (1 << (8 * length)) - 1
    if not 0 <= value <= max_value:
        allowed_range = f'[0..{max_value}]'
        err_msg = f'{value} is not valid for {length} byte(s) {allowed_range}'
        raise Chip8Panic(err_msg)

    return value
