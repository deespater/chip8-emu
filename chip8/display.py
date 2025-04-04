class Chip8Display:
    WIDTH: int = 64
    HEIGHT: int = 32

    memory: list[bytearray]

    def __init__(self) -> None:
        self.clear()

    def draw_sprite(
        self,
        sprite_data: bytes,
        sprite_x: int,
        sprite_y: int,
    ) -> None:
        """Setting sprite data to display memory"""

        for row_index, sprite_row_bytes in enumerate(sprite_data):
            # Length of sprite_data is the height of sprite so we iterating
            # each row of sprite
            for column_index in range(8):  # Sprite is fixed 8 bit width
                # Wrapping bits horizontally
                dx = (sprite_x + column_index) % self.WIDTH
                # Wrapping bits vertically
                dy = (sprite_y + row_index) % self.HEIGHT

                sprite_pixel = (sprite_row_bytes >> (7 - column_index)) & 1
                self.memory[dy][dx] = sprite_pixel

    def clear(self) -> None:
        """Clearing memory and setting it to 0"""
        self.memory = [bytearray(self.WIDTH) for _ in range(self.HEIGHT)]

    def render(self) -> None:
        """Rendering display memory to the screen"""
        print('\033[H', end='')  # ANSI clear screen
        for row in self.memory:
            print(''.join('▓' if pixel else ' ' for pixel in row))
