def to_hex_str(n: int) -> str:
    s = ""
    for i in range(0, 32, 4):
        nibble_value = 0
        for j in range(4):
            nibble_value += ((n >> (i + j)) & 1) << j
        s += "0123456789ABCDEF"[nibble_value]
    return "0x" + s[::-1]
