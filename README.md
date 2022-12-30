# `mips`

MIPS simulator written in Python. As of writing, this can interpret machine code provided in hex and supports most common MIPS instructions. I hope.

Create an input file named `input.txt` and put your program's machine code in that file. An example is like so:

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

Once the file is set up, run `python3 main.py > output.txt` in your terminal of choice and the simulation output will show up in `output.txt`.

As of writing, `mips` outputs the entire [architectural state](https://en.wikipedia.org/wiki/Architectural_state) after each instruction.

I used [Digital Design and Computer Architecture](https://www.amazon.com/Digital-Design-Computer-Architecture-Harris/dp/0123944244) extensively as a reference. Thanks, Harris & Harris!