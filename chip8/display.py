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
        """
        Setting sprite data to display memory
        Length of sprite_data is the height of sprite so we iterating
        each row of sprite
        """
        collision_detected = False

        for row_index, sprite_byte in enumerate(sprite_data):
            for bit_index in range(8):  # Sprite is fixed 8 bit width
                sprite_pixel = (sprite_byte >> (7 - bit_index)) & 1

                if sprite_pixel == 0:
                    continue  # Skip if pixel is off

                # Wrapping bits horizontally and vertically
                dx = (sprite_x + bit_index) % self.WIDTH
                dy = (sprite_y + row_index) % self.HEIGHT

                # If pixel is already on, we set collision_detected
                if self.pixels[dy][dx] == 1:
                    collision_detected = True

                # XORing the screen pixel with sprite pixel
                self.pixels[dy][dx] ^= sprite_pixel

        # If collision is detected, we return glag to set the VF register to 1
        return collision_detected

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
