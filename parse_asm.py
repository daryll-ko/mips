from Instruction import *
from data import *


def parse_asm(asm: str) -> int:
    args = asm.split()
    for i in range(len(args)):
        if args[i][-1] == ',':
            args[i] = args[i][:-1]
    op = decode_op.inverse[args[0]][0] if args[0] in decode_op.inverse.keys() else 0
    if len(args) >= 3:  # not J-type
        if op == 0:  # R-type
            rs = decode_reg.inverse[args[2]][0]
            rt = decode_reg.inverse[args[3]][0]
            rd = decode_reg.inverse[args[1]][0]
            shamt = 0
            funct = decode_r.inverse[args[0]][0]
            return (rs << 21) + (rt << 16) + (rd << 11) + (shamt << 6) + funct
        else:  # I-type
            if op == 35:  # lw
                pass
            elif op == 43:  # sw
                pass
            else:
                rs = decode_reg.inverse[args[2]][0]
                rt = decode_reg.inverse[args[1]][0]
                imm = int(args[3])
                return (op << 26) + (rs << 21) + (rt << 16) + imm
    else:  # J-type
        pass
