from data import decode_reg
from to_inst import to_inst
from instruction import RType, IType, JType
from collections import defaultdict
from two_c_num import TwoCNumber


class Mips:
    def __init__(self) -> None:
        self.program_counter = 0x00400000
        self.registers = [TwoCNumber(0) for _ in range(32)]
        self.memory = defaultdict(int)

    def load_program(self, program: list[int]) -> None:
        index = 0x00400000
        for instruction in program:
            self.memory[index] = instruction
            index += 4

    def increment_pc(self, by: int = 4) -> None:
        self.program_counter += by

    def handle_inst(self, inst: RType | IType | JType) -> None:
        print(f"Instruction: {inst}\n")
        if isinstance(inst, RType):
            match inst.funct:
                case 8:
                    self.program_counter = self.registers[inst.rs]
                case 32 | 33:
                    self.registers[inst.rd] = (
                        self.registers[inst.rs] + self.registers[inst.rt]
                    )
                    self.increment_pc()
                case 34 | 35:
                    self.registers[inst.rd] = (
                        self.registers[inst.rs] - self.registers[inst.rt]
                    )
                    self.increment_pc()
                case 36:
                    self.registers[inst.rd] = (
                        self.registers[inst.rs] & self.registers[inst.rt]
                    )
                    self.increment_pc()
                case 37:
                    self.registers[inst.rd] = (
                        self.registers[inst.rs] | self.registers[inst.rt]
                    )
                    self.increment_pc()
                case 38:
                    self.registers[inst.rd] = (
                        self.registers[inst.rs] ^ self.registers[inst.rt]
                    )
                    self.increment_pc()
                case 39:
                    self.registers[inst.rd] = (
                        ~(self.registers[inst.rs] | self.registers[inst.rt])
                    )
                    self.increment_pc()
                case 42 | 43:
                    self.registers[inst.rd] = (
                        1 if self.registers[inst.rs] < self.registers[inst.rt]
                        else 0
                    )
                    self.increment_pc()
                case _:
                    print("no op executed")
                    self.increment_pc()
        elif isinstance(inst, IType):
            imm_as_2c = TwoCNumber(inst.imm)
            match inst.op:
                case 4:
                    self.program_counter += 4 + (
                        4 * inst.imm
                        if self.registers[inst.rs] == self.registers[inst.rt]
                        else 0
                    )
                case 5:
                    self.program_counter += 4 + (
                        4 * inst.imm
                        if self.registers[inst.rs] != self.registers[inst.rt]
                        else 0
                    )
                case 8:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] + imm_as_2c
                    )
                    self.increment_pc()
                case 12:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] & imm_as_2c
                    )
                    self.increment_pc()
                case 13:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] | imm_as_2c
                    )
                    self.increment_pc()
                case 14:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] ^ imm_as_2c
                    )
                    self.increment_pc()
                case 15:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] << 16
                    )
                    self.increment_pc()
                case 35:
                    self.registers[inst.rt] = (
                        self.memory[int(imm_as_2c + self.registers[inst.rs])]
                    )
                    self.increment_pc()
                case 43:
                    self.memory[int(imm_as_2c + self.registers[inst.rs])] = (
                        self.registers[inst.rt]
                    )
                    self.increment_pc()
                case _:
                    print('?', inst.op)
                    self.increment_pc()
        else:
            self.increment_pc()

    def run_program(self) -> None:
        while self.program_counter in self.memory:
            inst = to_inst(self.memory[self.program_counter])
            self.handle_inst(inst)
            print(self)
            print(f"{'-' * 40}\n")

    def __str__(self) -> str:
        nl = '\n'
        regfile_output = []
        for i in range(32):
            if int(self.registers[i]) != 0:
                regfile_output.append(
                    f"{decode_reg[i]}: {int(self.registers[i])}")
        memfile_output = []
        for key, value in self.memory.items():
            part_of_program = (
                int('0x00400000', 16) <= key <= int('0x0ffffffc', 16)
            )
            memfile_output.append(
                f"{format(key, '#010x')}: {format(value, '#010x')}"
                f"{' (program)' if part_of_program else ''}"
            )
        return f"""Program counter:

{format(self.program_counter, "#010x")}

Register file:

{
nl.join(regfile_output)
if len(regfile_output) > 0
else "(All registers contain 0.)"
}

Memory file:

{nl.join(memfile_output)}
"""
