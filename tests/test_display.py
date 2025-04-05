from chip8.display import Chip8Display


def test_display_initialization():
    display = Chip8Display()

    assert len(display.pixels) == display.HEIGHT
    assert all(len(row) == display.WIDTH for row in display.pixels)
    assert all(pixel == 0 for row in display.pixels for pixel in row)


def test_display_clear():
    display = Chip8Display()
    display.pixels[0][0] = 1  # Modify memory
    display.clear()

    assert all(pixel == 0 for row in display.pixels for pixel in row)


def test_draw_sprite_no_wrapping():
    display = Chip8Display()
    sprite_data = bytes([0b11110000])  # A single row sprite
    display.draw_sprite(sprite_data, 0, 0)

    assert display.pixels[0][0:4] == bytearray([1, 1, 1, 1])
    assert display.pixels[0][4:] == bytearray(display.WIDTH - 4)


def test_draw_sprite_horizontal_wrapping():
    display = Chip8Display()
    sprite_data = bytes([
        0b11000011,
        0b00111100,
    ])
    display.draw_sprite(sprite_data, 60, 0)  # Near the right edge

    assert display.pixels[0][60:64] == bytearray([1, 1, 0, 0])
    assert display.pixels[0][0:4] == bytearray([0, 0, 1, 1])
    assert display.pixels[1][60:64] == bytearray([0, 0, 1, 1])
    assert display.pixels[1][0:4] == bytearray([1, 1, 0, 0])


def test_draw_sprite_vertical_wrapping():
    display = Chip8Display()
    sprite_data = bytes([
        0b11000011,
        0b00111100,
    ])
    display.draw_sprite(sprite_data, 0, 31)  # Near the bottom edge

    assert display.pixels[31][0:8] == bytearray([1, 1, 0, 0, 0, 0, 1, 1])
    assert display.pixels[0][0:8] == bytearray([0, 0, 1, 1, 1, 1, 0, 0])


def test_render_output(capsys):
    display = Chip8Display()
    sprite_data = bytes([0b11110011])
    display.draw_sprite(sprite_data, 22, 11)
    display.render()

    buffer = capsys.readouterr()
    stdout_data = buffer.out

    screen_size = display.WIDTH * display.HEIGHT
    clear_seq_len = len(display.ASCII_CLEAR)
    newline_seq_len = display.HEIGHT - 1  # 1 byte for each row except the last

    expected_stdout_length = clear_seq_len + screen_size + newline_seq_len
    assert len(stdout_data) == expected_stdout_length

    # Converting stdout str back into display memory list[bytearray]
    stdout_rows = stdout_data[clear_seq_len:].split('\n')
    display_data = [
        bytearray([1 if char == display.PIXEL_CHAR else 0 for char in row])
        for row in stdout_rows
    ]
    assert len(display_data) == 32
    assert all(len(row) == 64 for row in display_data)
    assert display_data[11][22:30] == bytearray([1, 1, 1, 1, 0, 0, 1, 1])


def test_draw_sprite_collision_flag():
    display = Chip8Display()
    sprite_data = bytes([0b11110000])  # A single row sprite

    # Draw the sprite for the first time (no collision expected)
    collision = display.draw_sprite(sprite_data, 0, 0)
    assert not collision  # No collision on first draw

    # Draw the same sprite again at almost the same position (with collision)
    collision = display.draw_sprite(sprite_data, 1, 0)
    assert collision  # Collision should be detected

    # Verify that the pixels were XORed back to 0 where collision occurred
    assert display.pixels[0][0:4] == bytearray([1, 0, 0, 0])
    assert display.pixels[0][5:] == bytearray(display.WIDTH - 5)


def test_draw_sprite_collision_flag_with_wrapping():
    display = Chip8Display()
    sprite_data = bytes([
        0b11000011,
        0b00111100,
    ])

    # Draw the sprite for the first time (no collision expected)
    collision = display.draw_sprite(sprite_data, 62, 31)  # Near edges
    assert not collision  # No collision on first draw

    # Draw the same sprite again at the same position (collision expected)
    collision = display.draw_sprite(sprite_data, 62, 31)
    assert collision  # Collision should be detected

    # Verify that the pixels were XORed back to 0 at wrapped positions
    assert display.pixels[31][62:64] == bytearray([0, 0])
    assert display.pixels[31][0:2] == bytearray([0, 0])
    assert display.pixels[0][62:64] == bytearray([0, 0])
    assert display.pixels[0][0:2] == bytearray([0, 0])
