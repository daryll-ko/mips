from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TwoCNumber:
    bits: list[int]  # little-endian
    width: int = 32

    def __init__(self, n: int) -> None:
        if n >= 0:
            self.bits = [(n >> i) & 1 for i in range(self.width)]
        else:
            n *= -1
            self.bits = [(n >> i) & 1 for i in range(self.width)]
            self.flip()
            self += TwoCNumber(1)

    def __int__(self) -> int:
        value = 0
        for i in range(self.width - 1):
            value += self.bits[i] * (1 << i)
        value += -self.bits[self.width - 1] * (1 << (self.width - 1))

    def __str__(self) -> str:
        s = ""
        for i in range(0, self.width, 4):
            nibble_value = 0
            for j in range(4):
                nibble_value += self.bits[i + j] << j
            s += "0123456789abcdef"[nibble_value]
        return "0x" + reversed(s)

    def __add__(self, other: TwoCNumber) -> TwoCNumber:
        return TwoCNumber(int(self) + int(other))

    def __sub__(self, other: TwoCNumber) -> TwoCNumber:
        return TwoCNumber(int(self) - int(other))

    def flip(self) -> None:
        for i in range(self.width):
            self.bits[i] ^= 1
