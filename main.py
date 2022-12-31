import argparse

from mips import Mips
from parse_asm import parse_asm

parser = argparse.ArgumentParser(description="Simulate MIPS code!")
parser.add_argument("-a", "--asm", dest="is_assembly", action="store_true")
args = parser.parse_args()

mips = Mips()
program = []

with open("input.txt", 'r') as input_file:
    for line in input_file.readlines():
        line = line.strip()
        if args.is_assembly:
            inst = parse_asm(line)
            if inst is not None:
                program.append(inst)
        else:
            program.append(int(line, 16))

mips.load_program(program)
mips.run_program()
