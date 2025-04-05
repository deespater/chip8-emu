import time

from .utils import QuartzClock, parse_byte


class Chip8Timer(QuartzClock):
    value: int

    def __init__(self) -> None:
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
