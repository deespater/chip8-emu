import time

from .errors import Chip8Panic


class QuartzClock:
    CLOCK_RATE: int = 60  # Hz

    time_of_last_tick: float

    def __init__(self) -> None:
        self.time_of_last_tick = time.time()

    def synchronize(self) -> None:
        # Actually tick only if 1/60th of a second has passed
        time_now = time.time()
        if time_now - self.time_of_last_tick >= 1 / self.CLOCK_RATE:
            self.time_of_last_tick = time_now

            self.tick()

    def tick(self) -> None:
        raise NotImplementedError('Tick method not implemented')

def parse_byte(value: int, length: int = 1) -> int:
    # Max value based on length: 1 byte = 0...255, 2 bytes = 0..65535
    max_value = (1 << (8 * length)) - 1
    if not 0 <= value <= max_value:
        allowed_range = f'[0..{max_value}]'
        err_msg = f'{value} is not valid for {length} byte(s) {allowed_range}'
        raise Chip8Panic(err_msg)

    return value
