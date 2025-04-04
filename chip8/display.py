class Chip8Display:
    WIDTH: int = 64
    HEIGHT: int = 32

    ASCII_CLEAR: str = '\033[H'
    PIXEL_CHAR: str = '▓'

    pixels: list[bytearray]

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
                self.pixels[dy][dx] = sprite_pixel

    def clear(self) -> None:
        """Clearing memory and setting it to 0"""
        self.pixels = [bytearray(self.WIDTH) for _ in range(self.HEIGHT)]

    def render(self) -> None:
        """Rendering display memory to the screen"""
        print(self.ASCII_CLEAR, end='')  # ANSI clear screen

        # Rendering all pixels into buffer list
        buffer: list[str] = []
        for row in self.pixels:
            row_pixels = [self.PIXEL_CHAR if pixel else ' ' for pixel in row]
            buffer.append(''.join(row_pixels))

        # Rendering each row in a new line except the last one
        print('\n'.join(buffer), end='')
