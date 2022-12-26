from typing import Union
from Instruction import RType, IType, JType


def parse(machine_code: str) -> Union[RType, IType, JType]:
    machine_code = format(int(machine_code, 16), "032b")

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
        imm = int(machine_code[16:], 2)
        return IType(op, rs, rt, imm)
