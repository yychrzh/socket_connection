# coding=UTF-8


# decimal to binary
def dec2bin(x):
  x -= int(x)
  bins = []
  while x:
    x *= 2
    bins.append(1 if x>=1. else 0)
    x -= int(x)
  return bins


# binary to decimal
def bin2dec(b):
  d = 0
  for i, x in enumerate(b):
    d += 2**(-i-1)*x
  return d


# float32: 32-bit, 1-bit sign, 8-bit exponent, 23-bit fraction
def test_float32():
    print(dec2bin(0.5))
    print(bin2dec([1, 1, 0, 1]))


def test_array():
    a = [1] + [2, 3] + [4, 5, 6]
    print(a[1:])


def test_bytes():
    a = [0, 64, 128, 192, 255]
    b = bytes(a)
    print(b)
    print("lens: ", len(b))
    print("b type: ", type(b))
    for i in range(len(b)):
        print(b[i])


if __name__ == "__main__":
    test_bytes()