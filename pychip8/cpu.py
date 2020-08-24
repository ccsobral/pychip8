import numpy as np

from pychip8 import fontset

class Cpu:
    """Class handling CPU and memory operations.
    """

    def __init__(self):
        #Allocate the 4KB max memory available to Chip8
        self._memory = np.zeros(4096, dtype=np.uint8)

        #The 16 general-purpose 8-bit registers
        self._v_regs = np.zeros(16, dtype=np.uint8)

        #16-bit memory register
        self._i_reg = np.zeros(1, dtype=np.uint16)

        #Special delay and sound timers
        self._delay_timer = np.zeros(1, dtype=np.uint8)
        self._sound_timer = np.zeros(1, dtype=np.uint8)

        #Special registers and stack
        self._program_counter = np.zeros(1, dtype=np.uint16)
        self._stack_pointer = np.zeros(1, dtype=np.uint8)
        self._stack = np.zeros(16, dtype=np.uint16)

        self._setup_opcode_table()
        self._opcode = np.zeros(1, dtype=np.uint16)
        #Helper variables to avoid multiple definitions in opcode definitions
        self._vx = np.zeros(1, dtype=np.uint8)
        self._vy = np.zeros(1, dtype=np.uint8)

        #Variables that are accessed by the IO
        self.pixel_buffer = np.zeros((32,64), dtype=np.bool)
        self.draw_flag = np.zeros(1, dtype=np.bool)
        self.key_presses = np.zeros(16, dtype=np.bool)

        #Load the font set at the start of memory block
        self._load_fontset()

    def _setup_opcode_table(self):
        """Creates a lookup dictionary of opcode instructions.
        """

        self._opcode_main_table = {
            0x0: self._lookup_opcode_0nnn,
            0x1: self._op_1nnn,
            0x2: self._op_2nnn,
            0x3: self._op_3xnn,
            0x4: self._op_4xnn,
            0x5: self._op_5xy0,
            0x6: self._op_6xnn,
            0x7: self._op_7xnn,
            0x8: self._lookup_opcode_8xyn,
            0x9: self._op_9xy0,
            0xA: self._op_annn,
            0xB: self._op_bnnn,
            0xC: self._op_cxnn,
            0xD: self._op_dxyn,
            0xE: self._lookup_opcode_exnn,
            0xF: self._lookup_opcode_fxnn,
        }
    
        self._opcode_0nnn_table = {
            0x00: self._op_0000,
            0xe0: self._op_00e0,
            0xee: self._op_00ee,
        }

        self._opcode_8xyn_table = {
            0x0: self._op_8xy0,
            0x1: self._op_8xy1,
            0x2: self._op_8xy2,
            0x3: self._op_8xy3,
            0x4: self._op_8xy4,
            0x5: self._op_8xy5,
            0x6: self._op_8xy6,
            0x7: self._op_8xy7,
            0xe: self._op_8xye,
        }

        self._opcode_exnn_table = {
            0x9e: self._op_ex9e,
            0xa1: self._op_exa1,
        }

        self._opcode_fxnn_table = {
            0x07: self._op_fx07,
            0x0a: self._op_fx0a,
            0x15: self._op_fx15,
            0x18: self._op_fx18,
            0x1e: self._op_fx1e,
            0x29: self._op_fx29,
            0x33: self._op_fx33,
            0x55: self._op_fx55,
            0x65: self._op_fx65,
        }

    def _load_fontset(self):
        fonts = fontset.fontset
        self._memory[:len(fonts)] = fonts

    def load_rom(self, rom_data: bytes):
        """Inserts rom code into memory, starting at byte 512
        """

        rom_size = len(rom_data)
        self._memory[0x200:rom_size+0x200] = np.frombuffer(rom_data, dtype=np.uint8)
        np.copyto(self._program_counter, 0x200)
    
    def decrease_timers(self):
        """Runs down both delay and sound timers.
        """
        if self._delay_timer:
            self._delay_timer -= 1
        if self._sound_timer:
            self._sound_timer -= 1

    def run_cycle(self):
        """Run a full CPU cycle (fetch-decode-execute).
        """
        self._fetch_opcode()
        self._execute_opcode()

    def _fetch_opcode(self):
        """ Combines two bytes to make an opcode.

        Take byte in location memory[x], e.g 0b00001000.
        Shift it a byte to the left: 0b00001000 00000000,
        OR byte in memory[x+1], e.g. 0b00000010
        Resulting in opcode 0b0000100000000010 or 0x0802
        """
        np.copyto(
            self._opcode,
            self._memory[self._program_counter].astype(self._opcode.dtype) << 8 
            | self._memory[self._program_counter+1]
        )
        print(hex(self._opcode[0]))

        #Enough opcodes use these to be worth initialising here once
        vx = (self._opcode & 0x0F00) >> 8
        vy = (self._opcode & 0x00F0) >> 4
        np.copyto(self._vx, vx.astype(np.uint8))
        np.copyto(self._vy, vy.astype(np.uint8))

    def _execute_opcode(self):
        """Associates the opcodes with the corresponding instructions
        """

        self._lookup_opcode()
        self._program_counter += 2

    def _lookup_opcode(self):
        idx = (self._opcode & 0xF000) >> 12
        self._opcode_main_table[idx[0]]()
    
    def _lookup_opcode_0nnn(self):
        idx = self._opcode & 0x00FF
        self._opcode_0nnn_table[idx[0]]()
    
    def _lookup_opcode_8xyn(self):
        idx = self._opcode & 0x000F
        self._opcode_8xyn_table[idx[0]]()

    def _lookup_opcode_exnn(self):
        idx = self._opcode & 0x00FF
        self._opcode_exnn_table[idx[0]]()

    def _lookup_opcode_fxnn(self):
        idx = self._opcode & 0x00FF
        self._opcode_fxnn_table[idx[0]]()

    """Here starts the definitions of the different opcodes"""
    def _op_0000(self):
        raise ValueError('\n\nEND OF CODE\n\n')

    #Clear the screen
    def _op_00e0(self):
        self.pixel_buffer[:] = False
        np.copyto(self.draw_flag, True)

    #Return from subroutine
    def _op_00ee(self):
        self._stack_pointer -= 1
        np.copyto(self._program_counter, self._stack[self._stack_pointer])

    #Jump to address
    def _op_1nnn(self):
        np.copyto(self._program_counter, (self._opcode & 0x0FFF) - 2)
    
    #Execute sub-routine
    def _op_2nnn(self):
        self._stack[self._stack_pointer] = self._program_counter
        self._stack_pointer += 1
        np.copyto(self._program_counter, (self._opcode & 0x0FFF) - 2)
    
    #Skip instruction if VX value == nn
    def _op_3xnn(self):
        if self._v_regs[self._vx] == self._opcode & 0x00FF:
            self._program_counter += 2

    #Skip instruction if VX value != nn
    def _op_4xnn(self):
        if self._v_regs[self._vx] != self._opcode & 0x00FF:
            self._program_counter += 2
    
    #Skip instruction if VX == VY
    def _op_5xy0(self):
        if self._v_regs[self._vx] == self._v_regs[self._vy]:
            self._program_counter += 2
    
    #Store nn in VX
    def _op_6xnn(self):
        self._v_regs[self._vx] = self._opcode & 0x00FF
    
    #Add nn to VX
    def _op_7xnn(self):
        self._v_regs[self._vx] += self._opcode & 0x00FF

    #Store VY in VX
    def _op_8xy0(self):
        self._v_regs[self._vx] = self._v_regs[self._vy]
    
    #Set VX to (VX | VY)
    def _op_8xy1(self):
        new_vx = self._v_regs[self._vx] | self._v_regs[self._vy]
        self._v_regs[self._vx] = new_vx
        
    #Set VX to (VX & VY)
    def _op_8xy2(self):
        new_vx = self._v_regs[self._vx] & self._v_regs[self._vy]
        self._v_regs[self._vx] = new_vx

    #Set VX to (VX XOR VY)
    def _op_8xy3(self):
        new_vx = self._v_regs[self._vx] ^ self._v_regs[self._vy]
        self._v_regs[self._vx] = new_vx

    #Add VY to VX; set VF = 1 if carry else 0
    def _op_8xy4(self):
        #Carry if VX > 0xFF - VY
        carry = self._v_regs[self._vx] >  0xFF - self._v_regs[self._vy]
        self._v_regs[-1] = carry
        self._v_regs[self._vx] += self._v_regs[self._vy]

    #Subtract VY from VX; set VF = 0 if borrow else 1
    def _op_8xy5(self):
        borrow = self._v_regs[self._vx] < self._v_regs[self._vy]
        self._v_regs[-1] = not borrow
        self._v_regs[self._vx] -= self._v_regs[self._vy]

    #Store (VY >> 1) in VX; set VF = (VY & 0x0F)
    def _op_8xy6(self):
        self._v_regs[-1] = self._v_regs[self._vy] & 0x0F
        self._v_regs[self._vx] = self._v_regs[self._vy] >> 1

    #Store (VY - VX) in VX; set VF = 0 if borrow else 1
    def _op_8xy7(self):
        borrow = self._v_regs[self._vy] < self._v_regs[self._vx]
        self._v_regs[-1] = not borrow
        self._v_regs[self._vx] = self._v_regs[self._vy] - self._v_regs[self._vx]

    #Store (VY << 1) in VX; set VF = (VY & 0xF0)
    def _op_8xye(self):
        self._v_regs[-1] = self._v_regs[self._vy] & 0xF0
        self._v_regs[self._vx] = self._v_regs[self._vy] << 1

    #Skip next instruction if VX != VY
    def _op_9xy0(self):
        if self._v_regs[self._vx] != self._v_regs[self._vy]:
            self._program_counter += 2

    #Store address nnn in I
    def _op_annn(self):
        np.copyto(self._i_reg, self._opcode & 0x0FFF)

    #Jump to address (nnn + V0)
    def _op_bnnn(self):
        np.copyto(
            self._program_counter, self._v_regs[0] + (self._opcode & 0x0FFF) - 2
            )

    #Set VX to random number nn
    def _op_cxnn(self):
        rand_nn = np.random.default_rng().integers(0x100, dtype=np.uint8)
        self._v_regs[self._vx] = rand_nn

    #Draw sprite at pos (VX,VY) with n bytes start at address in I
    #Set VF = 1 if (set pixels are unset) else 0
    def _op_dxyn(self):
        sprite_height = self._opcode[0] & 0x000F
        #Position should wrap around if vx, vy larger than screen
        x_pos = self._v_regs[self._vx][0] % 64
        y_pos = self._v_regs[self._vy][0] % 32

        #Set VF = 0 unless any ON pixel is turned OFF
        self._v_regs[-1] = 0
        #Reminder that each sprite in the fontset is a column of 5 bytes
        for row in range(sprite_height):
            sprite_byte = self._memory[self._i_reg+row]
            for pixel_bit in range(8):
                #(128 >> pixel_bit) -> 128, 64, 32, 16...
                #so this picks up each bit in sprite_byte one by one
                if (sprite_byte & (128 >> pixel_bit)) != 0:
                    #if already set, XOR will unset it so make VF = 1
                    if y_pos + row >= self.pixel_buffer.shape[0]:
                        continue
                    if x_pos + pixel_bit >= self.pixel_buffer.shape[1]:
                        continue
                    if self.pixel_buffer[y_pos+row][x_pos+pixel_bit] != 0:
                        self._v_regs[-1] = 1
                    #XOR with current pixel value
                    self.pixel_buffer[y_pos+row][x_pos+pixel_bit] ^= 1

        np.copyto(self.draw_flag, True)
                    

    #Skip next instruction if key pressed == hex value in VX
    def _op_ex9e(self):
        key = self._v_regs[self._vx]
        if self.key_presses[key]:
            self._program_counter += 2

    #Skip next instruction if key == hex in VX is NOT pressed
    def _op_exa1(self):
        key = self._v_regs[self._vx]
        if not self.key_presses[key]:
            self._program_counter += 2

    #Store delay_timer in VX
    def _op_fx07(self):
        self._v_regs[self._vx] = self._delay_timer

    #Wait for keypress and store key in VX
    def _op_fx0a(self):
        #np.where returns a tuple of arrays
        #hence why accessing the index requires two indices
        key_array = np.where(self.key_presses == True)[0]
        if key_array.size > 0:
            self._v_regs[self._vx] = key_array[0]
        else:
            self._program_counter -= 2

    #Set delay_timer to value in VX
    def _op_fx15(self):
        np.copyto(self._delay_timer, self._v_regs[self._vx])

    #Set sound_timer to value in VX
    def _op_fx18(self):
        np.copyto(self._sound_timer, self._v_regs[self._vx])

    #Add value in VX to value in register I
    def _op_fx1e(self):
        self._i_reg += self._v_regs[self._vx]

    #Set I to address of sprite data corresponding to hex in VX
    def _op_fx29(self):
        """The fontset starts at._memory[0], each digit is 5 bytes long
        so the address of each digit sprite is simply the digit*5
        """
        np.copyto(self._i_reg, 5*self._v_regs[self._vx])

    #Store binary-coded decimal of value in VX in._memory at I, I+1, and I+2
    def _op_fx33(self):
        self._memory[self._i_reg] = (self._v_regs[self._vx] % 1000) // 100
        self._memory[self._i_reg+1] = (self._v_regs[self._vx] % 100) // 10
        self._memory[self._i_reg+2] = (self._v_regs[self._vx] % 10)

    #Store values V0 to VX (inclusive) in _memory at I, I+1, ...; set I to I+X+1
    def _op_fx55(self):
        ireg = self._i_reg[0]
        vx = self._vx[0] + 1
        self._memory[ireg:ireg+vx] = self._v_regs[:vx]
        np.copyto(self._i_reg, self._i_reg + self._vx + 1)

    #Fill V0 to VX (inc.) with values in memory at I, I+1, ...; set I to I+X+1
    def _op_fx65(self):
        ireg = self._i_reg[0]
        vx = self._vx[0] + 1
        self._v_regs[:vx] = self._memory[ireg:ireg+vx]
        np.copyto(self._i_reg, self._i_reg + self._vx + 1)