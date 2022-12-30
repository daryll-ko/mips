from Mips import Mips

mips = Mips()
program = []

with open("input.txt", 'r') as input_file:
    for line in input_file.readlines():
        program.append(int(line.strip(), 16))

mips.load_program(program)
mips.run_program()
