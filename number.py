from dataclasses import dataclass


@dataclass
class Number:
    width: int
    bits: list[int]
    twos_complement: bool

    def __int__(self) -> int:
        value = 0
        for i in range(self.width - 1):
            value += self.bits[i] * (1 << i)
        value += self.bits[self.width - 1] * \
            (1 << (self.width - 1)) * (-1 if self.twos_complement else 1)

    def __str__(self) -> str:
        return ''.join(map(str, self.bits))
