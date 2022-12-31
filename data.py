from bidict import bidict

decode_reg = bidict({
    0: "$0",
    1: "$at",
    2: "$v0",
    3: "$v1",
    4: "$a0",
    5: "$a1",
    6: "$a2",
    7: "$a3",
    8: "$t0",
    9: "$t1",
    10: "$t2",
    11: "$t3",
    12: "$t4",
    13: "$t5",
    14: "$t6",
    15: "$t7",
    16: "$s0",
    17: "$s1",
    18: "$s2",
    19: "$s3",
    20: "$s4",
    21: "$s5",
    22: "$s6",
    23: "$s7",
    24: "$t8",
    25: "$t9",
    26: "$k0",
    27: "$k1",
    28: "$gp",
    29: "$sp",
    30: "$fp",
    31: "$ra",
})

decode_op = bidict({
    1: ("bltz", "bgez"),
    2: "j",
    3: "jal",
    4: "beq",
    5: "bne",
    6: "blez",
    7: "bgtz",
    8: "addi",
    9: "addiu",
    10: "slti",
    11: "sltiu",
    12: "andi",
    13: "ori",
    14: "xori",
    15: "lui",
    16: ("mfc0", "mtc0"),
    17: ("bclf", "bclt"),
    28: "mul",
    32: "lb",
    33: "lh",
    35: "lw",
    36: "lbu",
    37: "lhu",
    40: "sb",
    41: "sh",
    43: "sw",
    49: "lwcl",
    56: "swcl",
})

decode_funct = bidict({
    0: "sll",
    2: "srl",
    3: "sra",
    4: "sllv",
    6: "srlv",
    7: "srav",
    8: "jr",
    9: "jalr",
    12: "syscall",
    13: "break",
    16: "mfhi",
    17: "mthi",
    18: "mflo",
    19: "mtlo",
    24: "mult",
    25: "multu",
    26: "div",
    27: "divu",
    32: "add",
    33: "addu",
    34: "sub",
    35: "subu",
    36: "and",
    37: "or",
    38: "xor",
    39: "nor",
    42: "slt",
    43: "sltu",
})
