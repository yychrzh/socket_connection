# coding=UTF-8


# decimal to binary
def dec2bin(x):
  x -= int(x)
  bins = []
  while x:
    x *= 2
    bins.append(1 if x >=1. else 0)
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


class A():
    def __init__(self, info):
        print("A", info)

    def func1(self):
        print("A.1")


class B():
    def __init__(self, info):
        print("B", info)

    def func2(self):
        print("B.2")


class C(A, B):
    def __init__(self, info):
        print(info)
        A.__init__(self, info)
        B.__init__(self, info)

    def func3(self):
        self.func1()
        self.func2()


def test_byte_char():
    from number_conversion import Number_conver
    n_c = Number_conver(False)
    o = [0, 64, 128, 192, 255]
    a = bytes(o)
    print([int(a[0])])
    b = [n_c.byte2char(v) for v in a]
    c = [n_c.char2byte(v) for v in b]
    print(o)
    print(b)
    print(c)


def test_const():
    import const
    const.PI = 3.14
    const.A_R = 0
    const.Rl = 0
    print(const.PI, const.A_R)
    print(const.Rl)


if __name__ == "__main__":
    # oc = C('fork')
    # oc.func3()
    # test_byte_char()
    # test_bytes()
    test_const()