### Known "out-of-spec" implementation
- CHIP-8 has it's own VRAM and does not use 4kb or RAM


### CHIP-8 instructions implementation progress

- [ ] 0nnn - SYS addr: Jump to a machine code routine at nnn
- [x] 00E0 - CLS: Clear the display
- [ ] 00EE - RET: Return from a subroutine
- [x] 1nnn - JP addr: Jump to location nnn
- [ ] 2nnn - CALL addr: Call subroutine at nnn
- [ ] 3xkk - SE Vx, byte: Skip next instruction if Vx = kk
- [ ] 4xkk - SNE Vx, byte: Skip next instruction if Vx != kk
- [ ] 5xy0 - SE Vx, Vy: Skip next instruction if Vx = Vy
- [x] 6xkk - LD Vx, byte: Set Vx = kk
- [x] 7xkk - ADD Vx, byte: Set Vx = Vx + kk
- [ ] 8xy0 - LD Vx, Vy: Set Vx = Vy
- [ ] 8xy1 - OR Vx, Vy: Set Vx = Vx OR Vy
- [ ] 8xy2 - AND Vx, Vy: Set Vx = Vx AND Vy
- [ ] 8xy3 - XOR Vx, Vy: Set Vx = Vx XOR Vy
- [ ] 8xy4 - ADD Vx, Vy: Set Vx = Vx + Vy, set VF = carry
- [ ] 8xy5 - SUB Vx, Vy: Set Vx = Vx - Vy, set VF = NOT borrow
- [ ] 8xy6 - SHR Vx {, Vy}: Set Vx = Vx SHR 1
- [ ] 8xy7 - SUBN Vx, Vy: Set Vx = Vy - Vx, set VF = NOT borrow
- [ ] 8xyE - SHL Vx {, Vy}: Set Vx = Vx SHL 1
- [ ] 9xy0 - SNE Vx, Vy: Skip next instruction if Vx != Vy
- [x] Annn - LD I, addr: Set I = nnn
- [ ] Bnnn - JP V0, addr: Jump to location nnn + V0
- [ ] Cxkk - RND Vx, byte: Set Vx = random byte AND kk
- [x] Dxyn - DRW Vx, Vy, nibble: Display n-byte sprite
- [ ] Ex9E - SKP Vx: Skip next instruction if key with the value of Vx is pressed
- [ ] ExA1 - SKNP Vx: Skip next instruction if key with the value of Vx is not pressed
- [x] Fx07 - LD Vx, DT: Set Vx = delay timer value
- [ ] Fx0A - LD Vx, K: Wait for a key press, store the value of the key in Vx
- [x] Fx15 - LD DT, Vx: Set delay timer = Vx
- [x] Fx18 - LD ST, Vx: Set sound timer = Vx
- [ ] Fx1E - ADD I, Vx: Set I = I + Vx
- [ ] Fx29 - LD F, Vx: Set I = location of sprite for digit Vx
- [ ] Fx33 - LD B, Vx: Store BCD representation of Vx in memory locations I, I+1, and I+2
- [ ] Fx55 - LD [I], Vx: Store registers V0 through Vx in memory starting at location I
- [ ] Fx65 - LD Vx, [I]: Read registers V0 through Vx from memory starting at location I
