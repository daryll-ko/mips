from data import decode_reg, decode_op, decode_r
from dataclasses import dataclass


@dataclass
class Instruction:
    op: int


@dataclass
class RType(Instruction):
    op: int
    rs: int
    rt: int
    rd: int
    shamt: int
    funct: int

    def __str__(self) -> str:
        return f"{decode_r[self.funct]} {decode_reg[self.rd]}, {decode_reg[self.rs]}, {decode_reg[self.rt]}"


@dataclass
class IType(Instruction):
    op: int
    rs: int
    rt: int
    imm: int

    def __str__(self) -> str:
        if 8 <= self.op <= 14:
            return f"{decode_op[self.op]} {decode_reg[self.rt]}, {decode_reg[self.rs]}, {self.imm}"
        elif 32 <= self.op <= 43:
            return f"{decode_op[self.op]} {decode_reg[self.rt]}, {self.imm}({decode_reg[self.rs]})"


@dataclass
class JType(Instruction):
    op: int
    addr: int
