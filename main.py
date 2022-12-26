from Mips import Mips

mips = Mips()
program = []

with open("input.txt", 'r') as input_file:
    lines = input_file.readlines()
    for line in lines:
        program.append(int(line, 16))

mips.load_program(program)
mips.run_program()
