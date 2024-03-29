import re

from data import decode_reg, decode_op, decode_funct


def parse_asm(asm: str) -> int:
    args = asm.split()
    for i in range(len(args)):
        if args[i][-1] == ',':
            args[i] = args[i][:-1]
    op = (decode_op.inverse[args[0]]
          if args[0] in decode_op.inverse.keys()
          else 0)
    if op == 0:  # R-type
        funct = decode_funct.inverse[args[0]]
        rs, rt, rd, shamt = -1, -1, -1, -1
        if 0 <= funct <= 3:
            rs = 0
            rt = decode_reg.inverse[args[2]]
            rd = decode_reg.inverse[args[1]]
            shamt = int(args[3])
        elif 4 <= funct <= 7:
            rs = decode_reg.inverse[args[3]]
            rt = decode_reg.inverse[args[2]]
            rd = decode_reg.inverse[args[1]]
            shamt = 0
        elif funct == 8:
            rs = decode_reg.inverse[args[1]]
            rt = 0
            rd = 0
            shamt = 0
        elif funct == 16 or funct == 18:
            rs = 0
            rt = 0
            rd = decode_reg.inverse[args[1]]
            shamt = 0
        elif funct == 17 or funct == 19:
            rs = decode_reg.inverse[args[1]]
            rt = 0
            rd = 0
            shamt = 0
        elif 24 <= funct <= 25:
            rs = decode_reg.inverse[args[1]]
            rt = decode_reg.inverse[args[2]]
            rd = 0
            shamt = 0
        else:
            rs = decode_reg.inverse[args[2]]
            rt = decode_reg.inverse[args[3]]
            rd = decode_reg.inverse[args[1]]
            shamt = 0
        return (rs << 21) + (rt << 16) + (rd << 11) + (shamt << 6) + funct
    elif len(args) >= 3:  # I-type
        rs, rt, imm = -1, -1, -1
        if op == 15:  # lui
            rs = 0
            rt = decode_reg.inverse[args[1]]
            imm = int(args[2])
        elif op == 35 or op == 43:  # lw/sw
            rt = decode_reg.inverse[args[1]]
            regex_result = re.search(r"(-?\d+)\((\$[0-9a-z][0-9a-z]?)\)", args[2])
            rs = decode_reg.inverse[regex_result.group(2)]
            imm = int(regex_result.group(1))
        else:
            rs = decode_reg.inverse[args[2]]
            rt = decode_reg.inverse[args[1]]
            imm = int(args[3])
        return (op << 26) + (rs << 21) + (rt << 16) + imm
    else:  # J-type
        pass
