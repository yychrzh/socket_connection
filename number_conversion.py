# coding=UTF-8
import math


DEBUG_PRINT = False


def debug_print(data):
    if DEBUG_PRINT:
        print(data)


# decimal to binary: x: decimal, bit: accuracy
def dec2bin(x, bit=24):
    x -= int(x)
    bins = []
    accuracy_bit = 0
    while x:
        x *= 2
        current_bit = 1 if x >= 1. else 0
        bins.append(current_bit)
        if (accuracy_bit == 0 and current_bit == 1) or accuracy_bit > 0:
            accuracy_bit += 1
            if accuracy_bit >= bit:
                break
        x -= int(x)
    if accuracy_bit < bit:
        for i in range(bit - accuracy_bit):
            bins.append(0)
    return bins


# binary to decimal
def bin2dec(bins):
    dec = 0
    for i, x in enumerate(bins):
        dec += 2**(-i-1)*x
    return dec


# integer to binary, return list(L->R, High->LOW)
def int2bin(x, bit=0):
    bins = []
    while x:
        bins.append(x % 2)
        x = x // 2
    if len(bins) < bit:
        for i in range(bit - len(bins)):
            bins.append(0)
    bins.reverse()
    return bins


# binary to integer, input bin list(L->R, High->LOW)
def bin2int(bins):
    b = bins
    b.reverse()
    int_num = 0
    for i in range(len(b)):
        int_num += b[i] * 2**i
    return int(int_num)


# x: float data, bit: 32 or 64, for float 32 or float 64
# float32: 1-bit sign, 8-bit exponent, 23-bit fraction
# float64: 1-bit sign, 11-bit exponent, 52-bit fraction
def float2bin(x, bit=32):
    if bit != 32 and bit != 64:
        raise Exception("float bit choose error !")

    frac_bit = 23 if bit == 32 else 52
    exp_bit = 8 if bit == 32 else 11
    exp_offset = 127 if bit == 32 else 1023
    exponent, fraction = [], []

    # get the sign-bit value
    sign = 1 if x < 0.0 else 0
    abs_x = x if x > 0 else -x

    if x == 0:
        exponent = [0 for _ in range(exp_bit)]
        fraction = [0 for _ in range(frac_bit)]
        float_bins = [sign] + exponent + fraction
        return float_bins
    elif abs_x == float("inf"):
        exponent = [1 for _ in range(exp_bit)]
        fraction = [0 for _ in range(frac_bit)]
        float_bins = [sign] + exponent + fraction
        return float_bins

    # get the binary list of integer and decimal
    int_x = int(abs_x)
    dec_x = abs_x - int_x
    debug_print(["int, dec: ", int_x, dec_x])

    int_bins = int2bin(int_x)
    debug_print(["int_bins: ", int_bins])
    dec_bins = dec2bin(dec_x, frac_bit + 1 - len(int_bins))
    debug_print(["dec_bins: ", dec_bins])

    # get the integer num of exponent and fraction
    int_exponent = len(int_bins) - 1 + exp_offset
    if len(int_bins) > 0:
        # get the fraction bins
        for i in range(len(int_bins)):
            if i > 0:  # remove the '1' in the highest bit
                fraction.append(int_bins[i])  # add the binary in int_bins
        for i in range(frac_bit - len(int_bins) + 1):
            fraction.append(dec_bins[i])      # # add the binary in dec_bins
    else:
        first_1_pos = 0
        for i in range(len(dec_bins)):
            if dec_bins[i] == 0:
                int_exponent += -1
            else:
                first_1_pos = i
                break
        debug_print(["first_1_position: ", first_1_pos])
        fraction = dec_bins[(first_1_pos + 1):(first_1_pos + frac_bit + 1)]

    if len(fraction) != frac_bit:
        debug_print(["error in get fraction bins"])

    # get exponent
    debug_print(["int_exponent: ", int_exponent])
    if int_exponent < 0 or int_exponent >= 2**exp_bit:
        raise Exception("exponent run out of range !")

    exponent = int2bin(int_exponent)
    exponent.reverse()
    for i in range(exp_bit - len(exponent)):
        exponent.append(0)
    exponent.reverse()
    debug_print(["exponent: ", exponent])
    debug_print(["fraction: ", fraction])
    # get float bins:
    float_bins = [sign] + exponent + fraction
    return float_bins


def bin2float(bins):
    lens = len(bins)
    if lens != 32 and lens != 64:
        raise Exception("bins input error !")
    frac_bit = 23 if lens == 32 else 52
    exp_bit = 8 if lens == 32 else 11
    exp_offset = 127 if lens == 32 else 1023

    sign = bins[0]
    exponent = bins[1:(1+exp_bit)]
    debug_print(["exponent: ", exponent])
    fraction = bins[(1+exp_bit):]
    debug_print(["fraction: ", fraction])

    int_exponent = bin2int(exponent) - exp_offset
    dec_fraction = bin2dec(fraction)
    debug_print(["int_exponent: ", int_exponent])
    debug_print(["dec: ", dec_fraction])

    # special case
    if int_exponent == -127 and dec_fraction == 0:
        return 0.0
    elif int_exponent == (2**exp_bit - 1 - 127) and dec_fraction == 0:
        return float("inf")
    elif int_exponent == (2**exp_bit - 1 - 127) and dec_fraction != 0:
        return float("nan")

    float_data = ((-1)**sign) * (2**int_exponent) * (1 + dec_fraction)
    return float_data


# from a bins_list to byte_list
def bin2byte(bins):
    lens = len(bins)
    if lens != 32 and lens != 64:
        raise Exception("bins input error !")
    index = 0
    bytes_list = []  # 0~255
    while index <= (lens - 8):
        b = bin2int(bins[index:(index + 8)])
        bytes_list.append(b)
        index += 8


# from [0 ~ 255] to [-128 ~ 127]
def byte2char(byte):
    bins = int2bin(byte, 8)
    sign = bins[0]
    bins[0] = 0
    char_data = bin2int(bins)
    if char_data == 0 and sign == 1:
        return -128
    else:
        return ((-1)**sign) * char_data


if __name__ == "__main__":
    # print(int2bin(22))
    # print(bin2int([1, 0, 1, 1, 0]))
    # print(dec2bin(0.1, 24))
    # print(bin2dec([0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]))
    import time
    start_time = time.time()
    b = [0, 64, 127, 192, 255, 128]
    c = []
    for i in range(len(b)):
        c.append(byte2char(b[i]))
    print(c)

    print("time: %.7f" % (time.time() - start_time))
