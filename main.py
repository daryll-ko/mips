from parse import parse

with open("input.txt", 'r') as input_file:
    lines = input_file.readlines()
    for line in lines:
        inst = parse(line.strip())
        print(inst)
