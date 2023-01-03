def parse_2c(b: str) -> int:
    N = len(b)
    b = b[::-1]
    value = 0
    for i in range(N):
        value += (int(b[i]) << i) * (-1 if i == N - 1 else 1)
    return value
