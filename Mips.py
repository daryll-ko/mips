class Mips:

    def __init__(self) -> None:
        self.program_counter = 0x00400000
        self.registers = [0x00000000 for _ in range(32)]
