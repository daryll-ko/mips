# `mips`

MIPS simulator written in Python. As of writing, this can interpret **machine code provided in hex** or **MIPS assembly code** and supports most common MIPS instructions.

## Usage

Create an input file named `input.txt` and put your program's machine code or assembly code in that file. An example for machine code is like so:

```text
0x8C0A0020
0x02328020
0x2268FFF4
0x016D4022
```

This corresponds to the following instructions:

```asm
lw $t2, 32($0)
add $s0, $s1, $s2
addi $t0, $s3, -12
sub $t0, $t3, $t5
```

Once the input file is set up, run `python3 src/main.py [-a] > output.txt` in your terminal of choice and the simulation output will show up in `output.txt`. Include the `-a` flag only if your input file already contains MIPS assembly code.

After each instruction, the program outputs the entire [architectural state](https://en.wikipedia.org/wiki/Architectural_state).

## Notes

I used [Digital Design and Computer Architecture](https://www.amazon.com/Digital-Design-Computer-Architecture-Harris/dp/0123944244) extensively as a reference. Thanks, Harris & Harris!