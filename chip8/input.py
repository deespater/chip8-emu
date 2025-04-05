import time

import blessed

from .utils import QuartzClock


class Chip8Keyboard(QuartzClock):
    CLOCK_RATE: int = 60  # Hz
    KEY_MAP: dict[str, int] = {  # noqa: RUF012
        '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x43,
        'q': 0x34, 'w': 0x35, 'e': 0x36, 'r': 0x44,
        'a': 0x37, 's': 0x38, 'd': 0x39, 'f': 0x45,
        'z': 0x41, 'x': 0x30, 'c': 0x42, 'v': 0x46,
    }

    terminal: blessed.Terminal

    waiting_for_input: bool
    captured_key: int

    def __init__(self) -> None:
        super().__init__()

        self.terminal = blessed.Terminal()

        self.waiting_for_input = False
        self.captured_key = 0

    def get_captured_key(self) -> int:
        captured_key = self.captured_key
        self.captured_key = 0  # Reset captured key after reading

        return captured_key

    def wait_for_input(self) -> None:
        self.captured_key = 0
        self.waiting_for_input = True

    def tick(self) -> None:
        # No need to read input, we're not waiting
        if not self.waiting_for_input:
            return

        # Read input from terminal
        with self.terminal.cbreak(), self.terminal.hidden_cursor():
            captured_key = self.terminal.inkey(timeout=1 / self.CLOCK_RATE)

        # We're interested only in defined keymap, ignore others keys
        # Once we capture a key, we stop waiting for input
        if captured_key and captured_key in self.KEY_MAP:
            self.captured_key = self.KEY_MAP.get(captured_key)
            self.wait_for_input = False
