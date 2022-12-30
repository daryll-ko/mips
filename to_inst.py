from Instruction import *


def from_2c(b: str) -> int:
    N = len(b)
    value = (1 if b[0] == '1' else 0) * -(1 << (N - 1))
    for i in range(1, N):
        value += (1 if b[i] == '1' else 0) * (1 << ((N - 1) - i))
    return value


def to_inst(machine_code: int) -> Instruction:
    machine_code = format(machine_code, "032b")

    if machine_code[:6] == "000000":  # R-type
        rs = int(machine_code[6:11], 2)
        rt = int(machine_code[11:16], 2)
        rd = int(machine_code[16:21], 2)
        shamt = int(machine_code[21:26], 2)
        funct = int(machine_code[26:], 2)
        return RType(0, rs, rt, rd, shamt, funct)

    elif machine_code[:6] in ["000010", "000011"]:  # J-type
        op = int(machine_code[:6], 2)
        addr = int(machine_code[6:], 2)
        return JType(op, addr)

    else:  # I-type
        op = int(machine_code[:6], 2)
        rs = int(machine_code[6:11], 2)
        rt = int(machine_code[11:16], 2)
        imm = from_2c(machine_code[16:])
        return IType(op, rs, rt, imm)
