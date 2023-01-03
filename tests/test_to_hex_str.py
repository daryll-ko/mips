from src.to_hex_str import to_hex_str


def test_to_hex_str():
    with open("tests/test_to_hex_str.txt", 'r') as test_input:
        for line in test_input.readlines():
            n, n_in_hex = line.split()
            n = int(n)
            assert to_hex_str(n) == n_in_hex
