from data import *
from to_inst import to_inst
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

    def increment_pc(self, by: int = 4) -> None:
        self.program_counter += by

    def handle_inst(self, inst: Instruction) -> None:
        print(f"Instruction: {inst}\n")
        if isinstance(inst, RType):
            match inst.funct:
                case 8:
                    self.program_counter = self.registers[inst.rs]
                case 32:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] + self.registers[inst.rt]
                    self.increment_pc()
                case 34:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] - self.registers[inst.rt]
                    self.increment_pc()
                case 36:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] & self.registers[inst.rt]
                    self.increment_pc()
                case 37:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] | self.registers[inst.rt]
                    self.increment_pc()
                case 38:
                    self.registers[inst.rd] = \
                        self.registers[inst.rs] ^ self.registers[inst.rt]
                    self.increment_pc()
                case 39:
                    self.registers[inst.rd] = \
                        ~(self.registers[inst.rs] | self.registers[inst.rt])
                    self.increment_pc()
                case 42:
                    self.registers[inst.rd] = 1 if self.registers[inst.rs] < self.registers[inst.rt] else 0
                    self.increment_pc()
                case _:
                    print('?', inst.funct)
                    self.increment_pc()
        elif isinstance(inst, IType):
            match inst.op:
                case 4:
                    self.program_counter = \
                        self.program_counter + 4 + \
                        (4 * inst.imm if self.registers[inst.rs]
                         == self.registers[inst.rt] else 0)
                case 5:
                    self.program_counter = \
                        self.program_counter + 4 + \
                        (4 * inst.imm if self.registers[inst.rs]
                         != self.registers[inst.rt] else 0)
                case 8:
                    self.registers[inst.rt] = self.registers[inst.rs] + inst.imm
                    self.increment_pc()
                case 12:
                    self.registers[inst.rt] = self.registers[inst.rs] & inst.imm
                    self.increment_pc()
                case 13:
                    self.registers[inst.rt] = self.registers[inst.rs] | inst.imm
                    self.increment_pc()
                case 14:
                    self.registers[inst.rt] = self.registers[inst.rs] ^ inst.imm
                    self.increment_pc()
                case 15:
                    self.registers[inst.rt] = self.registers[inst.rs] << 16
                    self.increment_pc()
                case 35:
                    self.registers[inst.rt] = self.memory[inst.imm +
                                                          self.registers[inst.rs]]
                    self.increment_pc()
                case 43:
                    self.memory[inst.imm + self.registers[inst.rs]
                                ] = self.registers[inst.rt]
                    self.increment_pc()
                case _:
                    print('?', inst.op)
                    self.increment_pc()
        else:
            self.increment_pc()

    def run_program(self) -> None:
        while self.program_counter in self.memory:
            inst = to_inst(hex(self.memory[self.program_counter]))
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

{nl.join(
    [f"{format(key, '#010x')}: {format(value, '#010x')}{' (program)' if int('0x00400000', 16) <= key <= int('0x0ffffffc', 16) else ''}" for key, value in self.memory.items()]
)}
"""
