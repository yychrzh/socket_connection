# coding=UTF-8
# use python2
import math


# single float: 32 bits, 4 bytes
FLOAT32_BIT = 32
FLOAT32_BYTE = 4
FLOAT32_EXPONENT = 8
FLOAT32_EXPONENT_OFFSET = 127
FLOAT32_FRACTION = 23
FLOAT32_BIN_BUF = 150    # FLOAT32_FRACTION + (int)(pow(2, FLOAT32_EXPONENT) - 1)  // 150
FLOAT32_BYTE_BUF = 4     # (int)(FLOAT32_BIN_BUF / 8) + 1   // 19

# double float: 64 bits, 8 bytes
FLOAT64_BIT = 64
FLOAT64_BYTE = 8
FLOAT64_EXPONENT = 11
FLOAT64_EXPONENT_OFFSET = 1023
FLOAT64_FRACTION = 52
FLOAT64_BIN_BUF = 1075        # FLOAT64_FRACTION + (int)(pow(2, FLOAT64_EXPONENT) - 1)  // 1075
FLOAT64_BYTE_BUF = 8          # (int)(FLOAT64_BIN_BUF / 8) + 1    // 135


class Number_conver(object):
    def __init__(self, print_flag=False):
        self.debug_print_flag = print_flag

    def debug_print(self, infostr, infodata, data_lens):
        if self.debug_print_flag:
            data_str = ""
            for i in range(data_lens):
                data_str += (str(infodata[i]) + " ")
            print("(num_conver)" + infostr + ": " + data_str)

    """*********************************bin**********************************"""
    # decimal to binary: x: decimal, bit: accuracy
    def dec2bin(self, input_data, bit=32):
        x = input_data - int(input_data)
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
    def bin2dec(self, bins):
        dec = 0
        for i, x in enumerate(bins):
            if x != 0:
                dec += 2 ** (-i - 1) * x
        return dec

    # integer to binary, return list(L->R, High->Low)
    def int2bin(self, input_data, bit=32):
        bins = []
        x = input_data
        while x:
            bins.append(x % 2)
            x = x // 2
        if len(bins) < bit:
            for i in range(bit - len(bins)):
                bins.append(0)
        bins.reverse()
        return bins

    # binary to integer, input bin list(L->R, High->Low)
    def bin2int(self, bins):
        b = bins
        b.reverse()
        int_num = 0
        for i in range(len(b)):
            if b[i] != 0:
                int_num += b[i] * 2 ** i
        return int(int_num)

    # x: float data, bit: 32 or 64, for float 32 or float 64
    # float32: 1-bit sign, 8-bit exponent, 23-bit fraction
    # float64: 1-bit sign, 11-bit exponent, 52-bit fraction
    def float2bin(self, input_data, bit=32):
        if bit != 32 and bit != 64:
            raise Exception("float bit choose error !")
        x = input_data

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

        int_bins = self.int2bin(int_x, 0)
        dec_bins = self.dec2bin(dec_x, frac_bit + 1 - len(int_bins))

        # get the integer num of exponent and fraction
        int_exponent = len(int_bins) - 1 + exp_offset
        if len(int_bins) > 0:
            # get the fraction bins
            for i in range(len(int_bins)):
                if i > 0:  # remove the '1' in the highest bit
                    fraction.append(int_bins[i])  # add the binary in int_bins
            for i in range(frac_bit - len(int_bins) + 1):
                fraction.append(dec_bins[i])  # # add the binary in dec_bins
        else:
            first_1_pos = 0
            for i in range(len(dec_bins)):
                if dec_bins[i] == 0:
                    int_exponent += -1
                else:
                    first_1_pos = i
                    break
            fraction = dec_bins[(first_1_pos + 1):(first_1_pos + frac_bit + 1)]

        # get exponent
        if int_exponent < 0 or int_exponent >= 2 ** exp_bit:
            raise Exception("exponent run out of range !")

        exponent = self.int2bin(int_exponent, 0)
        exponent.reverse()
        for i in range(exp_bit - len(exponent)):
            exponent.append(0)
        exponent.reverse()
        # get float bins:
        float_bins = [sign] + exponent + fraction
        return float_bins

    def bin2float(self, bins):
        lens = len(bins)
        if lens != 32 and lens != 64:
            raise Exception("bins input error !")
        frac_bit = 23 if lens == 32 else 52
        exp_bit = 8 if lens == 32 else 11
        exp_offset = 127 if lens == 32 else 1023

        sign = bins[0]
        exponent = bins[1:(1 + exp_bit)]
        fraction = bins[(1 + exp_bit):]

        int_exponent = self.bin2int(exponent) - exp_offset
        dec_fraction = self.bin2dec(fraction)

        # special case
        if int_exponent == -127 and dec_fraction == 0:
            return 0.0
        elif int_exponent == (2 ** exp_bit - 1 - 127) and dec_fraction == 0:
            print("inf !")
            return float("inf")
        elif int_exponent == (2 ** exp_bit - 1 - 127) and dec_fraction != 0:
            print("nan !")
            return float("nan")

        float_data = ((-1) ** sign) * (2 ** int_exponent) * (1 + dec_fraction)
        return float_data

    def byte2bin(self, input_data):
        bins = []
        byte_data = input_data
        i = 0
        while byte_data:
            bins.append(byte_data % 2)
            byte_data = int(byte_data / 2)
            i += 1
        if i < 8:
            for j in range(8 - i):
                bins.append(0)
        bins.reverse()
        return bins

    def bin2byte(self, bins):
        byte_data = 0
        for i in range(8):
            if bins[i] != 0:
                byte_data += bins[i] * (2**(7 - i))
        return byte_data

    def bys2bin(self, bys):
        bins = []
        for i in range(len(bys)):
            temp_bin = self.byte2bin(bys[i])
            for j in range(8):
                bins.append(temp_bin[j])
        return bins

    def bin2bys(self, bins):
        if (len(bins) % 8) is not None:
            raise Exception("bins lens input error !")
        bys = []
        for i in range(int(len(bins) / 8)):
            byte_data = self.bin2byte(bins[8 * i:(8 * i + 8)])
            bys.append(byte_data)
        return bys

    """*********************************byte**********************************"""
    def dec2byte(self, input_data, bit=32):
        if bit != 32 and bit != 64:
            raise Exception("float bit choose error !")
        x = input_data
        bins = self.dec2bin(x, bit)
        bys = []
        for i in range(int(bit / 8)):
            bys.append(self.bin2byte(bins[8 * i:(8 * i + 8)]))
        return bys

    def byte2dec(self, bys):
        dec_data = 0.0
        for i in range(len(bys)):
            if bys[i] != 0:
                dec_data += bys[i] * (256**(-i - 1))
        return dec_data

    def int2byte(self, input_data, bit=32):
        if bit != 32 and bit != 64:
            raise Exception("float bit choose error !")
        x = input_data
        bins = self.int2bin(x, bit)
        bys = []
        for i in range(int(bit / 8)):
            bys.append(self.bin2byte(bins[8 * i:(8 * i + 8)]))
        return bys

    def byte2int(self, bys):
        int_data = 0
        for i in range(len(bys)):
            if bys[i] != 0:
                int_data += bys[i] * (256**(len(bys) - i - 1))
        return int_data

    def float2byte(self, input_data, bit=32):
        if bit != 32 and bit != 64:
            raise Exception("float bit choose error !")
        x = input_data

        bins = self.float2bin(x, bit)
        bys = []
        for i in range(int(bit / 8)):
            bys.append(self.bin2byte(bins[8 * i:(8 * i + 8)]))
        return bys

    def byte2float(self, bys):
        bins = self.bys2bin(bys)
        float_data = self.bin2float(bins)
        return float_data

    # data_lens: float data_lens:
    def float_array2bys(self, float_array, bit=32):
        if bit != 32 and bit != 64:
            raise Exception("float bit choose error !")
        bys = []
        for i in range(len(float_array)):
            temp_bys = self.float2byte(float_array[i], bit)
            for j in range(len(temp_bys)):
                bys.append(temp_bys[j])
        return bys

    def bys2float_array(self, bys, bit=32):
        if bit != 32 and bit != 64:
            raise Exception("float bit choose error !")
        buf = 4 if bit == 32 else 8
        float_array = []
        for i in range(int(len(bys) / buf)):
            float_array.append(self.byte2float(bys[(buf * i):(buf * i + buf)]))
        return float_array

    """*********************************char**********************************"""
    # from [-128, 127] to [0, 255]
    def char2byte(self, input_data):
        if input_data == -128:
            return 128
        elif input_data < 0:
            return 128 - input_data
        else:
            return input_data

    # from [0, 255] to [-128, 127]
    def byte2char(self, input_data):
        bins = self.byte2bin(input_data)
        sign = bins[0]
        bins[0] = 0
        char_data = self.bin2byte(bins)
        if char_data == 0 and sign == 1:
            return -128
        else:
            return ((-1) ** sign) * char_data


if __name__ == "__main__":
    n_c = Number_conver(True)
    """
    f1 = 178.125
    f2 = 178.123456
    bin1 = n_c.float2bin(f1, 32)
    bin2 = n_c.float2bin(f2, 32)
    bin3 = n_c.float2bin(f2, 64)
    n1 = n_c.bin2float(bin1)
    n2 = n_c.bin2float(bin2)
    n3 = n_c.bin2float(bin3)
    print(n1, n2, n3)
    
    f1 = 0.123456789123456789123456789

    bys = n_c.dec2byte(f1, 64)
    print(bys)
    f2 = n_c.byte2dec(bys)
    print("%.20f" % f2)
    int1 = 123456789123456
    bys = n_c.int2byte(int1, 64)
    print(bys)
    int2 = n_c.byte2int(bys)
    print(int2)

    f1 = 178.12597866655
    print(f1)
    bys = n_c.float2byte(f1)
    bys64 = n_c.float2byte(f1, 64)
    f32 = n_c.byte2float(bys)
    f64 = n_c.byte2float(bys64)
    print(bys)
    print(bys64)
    print(f32)
    print(f64)
    
    x1 = [-128, -64, 0, 64, 127]  # char
    x2 = [0, 64, 128, 192, 255]   # byte
    b1 = [n_c.char2byte(v) for v in x1]
    c1 = [n_c.byte2char(v) for v in b1]
    print(b1)
    print(c1)
    """
    a = [11.01, 2.025, 178.245]

    bys32 = n_c.float_array2bys(a, 32)
    bys64 = n_c.float_array2bys(a, 64)

    d32 = n_c.bys2float_array(bys32, 32)
    d64 = n_c.bys2float_array(bys64, 64)

    print(d32)
    print(d64)
