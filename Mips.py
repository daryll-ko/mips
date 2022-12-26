from data import *
from parse import parse
from Instruction import *
from collections import defaultdict


class Mips:
    def __init__(self) -> None:
        self.program_counter = 0x00400000
        self.registers = [0x00000000 for _ in range(32)]
        self.memory = defaultdict(int)

    def load_program(self, program: list[int]) -> None:
        index = 0x00400000
        for instruction in program:
            self.memory[index] = instruction
            index += 4

    def handle_inst(self, inst: Instruction) -> None:
        print(f"Instruction: {inst}\n")
        if isinstance(inst, RType):
            match inst.funct:
                case 8:
                    self.program_counter = self.registers[inst.rs]
                case 32:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] + self.registers[inst.rt]
                    self.program_counter += 4
                case 34:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] - self.registers[inst.rt]
                    self.program_counter += 4
                case 36:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] & self.registers[inst.rt]
                    self.program_counter += 4
                case 37:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] | self.registers[inst.rt]
                    self.program_counter += 4
                case 38:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] ^ self.registers[inst.rt]
                    self.program_counter += 4
                case 39:
                    self.registers[inst.rd] = \
                        ~(self.registers[inst.rs] | self.registers[inst.rt])
                    self.program_counter += 4
                case 42:
                    self.registers[inst.rd] = 1 if self.registers[inst.rs] < self.registers[inst.rt] else 0
                    self.program_counter += 4
                case _:
                    print('?', inst.funct)
                    self.program_counter += 4
        elif isinstance(inst, IType):
            match inst.op:
                case 4:
                    self.program_counter = \
                        (self.program_counter + 4 + 4 * inst.imm) \
                        if self.registers[inst.rs] == self.registers[inst.rt] \
                        else (self.program_counter + 4)
                case 5:
                    self.program_counter = \
                        (self.program_counter + 4 + 4 * inst.imm) \
                        if self.registers[inst.rs] != self.registers[inst.rt] \
                        else (self.program_counter + 4)
                case 8:
                    self.registers[inst.rt] = self.registers[inst.rs] + inst.imm
                    self.program_counter += 4
                case 12:
                    self.registers[inst.rt] = self.registers[inst.rs] & inst.imm
                    self.program_counter += 4
                case 13:
                    self.registers[inst.rt] = self.registers[inst.rs] | inst.imm
                    self.program_counter += 4
                case 14:
                    self.registers[inst.rt] = self.registers[inst.rs] ^ inst.imm
                    self.program_counter += 4
                case 15:
                    self.registers[inst.rt] = self.registers[inst.rs] << 16
                    self.program_counter += 4
                case 35:
                    self.registers[inst.rt] = self.memory[inst.imm +
                                                          self.registers[inst.rs]]
                    self.program_counter += 4
                case 43:
                    self.memory[inst.imm + self.registers[inst.rs]
                                ] = self.registers[inst.rt]
                    self.program_counter += 4
                case _:
                    print('?', inst.op)
                    self.program_counter += 4
        else:
            self.program_counter += 4

    def run_program(self) -> None:
        while self.program_counter in self.memory:
            inst = parse(hex(self.memory[self.program_counter]))
            self.handle_inst(inst)
            print(self)
            print(f"{'-' * 40}\n")

    def __str__(self) -> str:
        nl = '\n'
        return f"""Program counter:

{format(self.program_counter, "#010x")}

Register file:

{nl.join([f"{decode_reg[i]}: {format(self.registers[i], '#010x')}" for i in range(32)])}

Memory file:

{nl.join([f"{key}: {value}" for key, value in self.memory.items()])}
"""
