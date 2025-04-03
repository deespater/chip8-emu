rom_bytes = bytes([
    0x60, 0x0A,  # LD V0, 0x0A (x)
    0x61, 0x08,  # LD V1, 0x08 (y)
    0xA5, 0x00,  # LD I, 0x300 (sprite location)
    0xD0, 0x15,  # DRW V0, V1, 5 (5-row sprite)
    0x12, 0x06   # JP 0x206 (loop forever)
])

smiley_sprite = bytes([
    0xFF,  # 11111111
    0x81,  # 10000001
    0xA5,  # 10100101
    0x81,  # 10000001
    0xFF,  # 11111111
])

# Write ROM file
with open("dummy.rom", "wb") as f:
    f.write(rom_bytes)
    f.write(b'\x00' * (0x300 - len(rom_bytes)))
    f.write(smiley_sprite)
