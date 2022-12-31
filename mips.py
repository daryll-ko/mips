from data import decode_reg
from to_inst import to_inst
from instruction import RType, IType, JType
from collections import defaultdict


def to_hex_str(n: int) -> str:
    s = ""
    for i in range(0, 32, 4):
        nibble_value = 0
        for j in range(4):
            nibble_value += ((n >> (i + j)) & 1) << j
        s += "0123456789ABCDEF"[nibble_value]
    return "0x" + s[::-1]


class Mips:
    def __init__(self) -> None:
        self.program_counter = 0x00400000
        self.registers = [0x00000000 for _ in range(32)]
        self.memory = defaultdict(int)
        self.hi = 0x00000000
        self.lo = 0x00000000

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
                case 0:
                    self.registers[inst.rd] = (
                        self.registers[inst.rt] << inst.shamt
                    )
                    self.increment_pc()
                case 2:
                    unsigned_value = self.registers[inst.rt] & 0xFFFFFFFF
                    self.registers[inst.rd] = (
                        unsigned_value >> inst.shamt
                    )
                    self.increment_pc()
                case 3:
                    self.registers[inst.rd] = (
                        self.registers[inst.rt] >> inst.shamt
                    )
                    self.increment_pc()
                case 4:
                    self.registers[inst.rd] = (
                        self.registers[inst.rt] << self.registers[inst.rs]
                    )
                    self.increment_pc()
                case 6:
                    unsigned_value = self.registers[inst.rt] & 0xFFFFFFFF
                    self.registers[inst.rd] = (
                        unsigned_value >> self.registers[inst.rs]
                    )
                    self.increment_pc()
                case 7:
                    self.registers[inst.rd] = (
                        self.registers[inst.rt] >> self.registers[inst.rs]
                    )
                    self.increment_pc()
                case 8:
                    self.program_counter = self.registers[inst.rs]
                case 16:
                    self.registers[inst.rd] = self.hi
                    self.increment_pc()
                case 17:
                    self.hi = self.registers[inst.rs]
                    self.increment_pc()
                case 18:
                    self.registers[inst.rd] = self.lo
                    self.increment_pc()
                case 19:
                    self.lo = self.registers[inst.rs]
                    self.increment_pc()
                case 24 | 25:
                    product = self.registers[inst.rs] * self.registers[inst.rt]
                    self.hi = product >> 32
                    self.lo = product & 0xFFFFFFFF
                    self.increment_pc()
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
                case 8 | 9:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] + inst.imm
                    )
                    self.increment_pc()
                case 12:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] & inst.imm
                    )
                    self.increment_pc()
                case 13:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] | inst.imm
                    )
                    self.increment_pc()
                case 14:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] ^ inst.imm
                    )
                    self.increment_pc()
                case 15:
                    self.registers[inst.rt] = (
                        self.registers[inst.rs] << 16
                    )
                    self.increment_pc()
                case 35:
                    self.registers[inst.rt] = (
                        self.memory[inst.imm + self.registers[inst.rs]]
                    )
                    self.increment_pc()
                case 43:
                    self.memory[inst.imm + self.registers[inst.rs]] = (
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
            if self.registers[i] != 0:
                regfile_output.append(
                    f"{decode_reg[i]}: {to_hex_str(self.registers[i])}")
        memfile_output = []
        for key, value in self.memory.items():
            part_of_program = (
                int('0x00400000', 16) <= key <= int('0x0FFFFFFC', 16)
            )
            memfile_output.append(
                f"{to_hex_str(key)}: {to_hex_str(value)}"
                f"{' (program)' if part_of_program else ''}"
            )
        return f"""Program counter:

{to_hex_str(self.program_counter)}

Register file:

{
nl.join(regfile_output)
if len(regfile_output) > 0
else "(All registers contain 0.)"
}

Memory file:

{nl.join(memfile_output)}
"""
