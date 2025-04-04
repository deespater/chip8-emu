import time

from .utils import parse_byte


class QuartzClock:
    CLOCK_RATE: int = 60  # Hz

    time_of_last_tick: float

    def __init__(self):
        self.time_of_last_tick = time.time()

    def synchronize(self) -> None:
        # Actually tick only if 1/60th of a second has passed
        time_now = time.time()
        if time_now - self.time_of_last_tick >= 1 / self.CLOCK_RATE:
            self.last_tick = time_now

            self.tick()

    def tick(self) -> None:
        raise NotImplementedError('Tick method not implemented')


class Chip8Timer(QuartzClock):
    value: int

    def __init__(self):
        super().__init__()
        self.value = 0

    def update(self, value: int) -> None:
        self.value = parse_byte(value)

    def tick(self) -> None:
        if self.value > 0:
            self.value -= 1


class DelayTimer(Chip8Timer):
    pass


class SoundTimer(Chip8Timer):
    def tick(self) -> None:
        super().tick()

        if self.value == 0:
            print('BEEP!')
