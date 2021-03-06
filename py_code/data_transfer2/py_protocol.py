from number_conversion import Number_conver
from py_tcpsocket import Tcpsocket


# data format: 0: data_flag;1: data_type;2: parity_flag;3: data_length high;4: data_length low;5~: byte data
TRANS_FLAG_LENGTH        = 1                                 # send data flag: 1bits
DATA_TYPE_LENGTH         = 1                                 # data type: float or double
PARITY_LENGTH            = 1                                 # parity check of data: 1bits: 0 or 1
DATA_LEN_FLAG_LENGTH     = 2                                 # max data lens: 65535 bytes, 16383 float or 8191 double

FLAG_LENGTH              = TRANS_FLAG_LENGTH + DATA_TYPE_LENGTH + PARITY_LENGTH + DATA_LEN_FLAG_LENGTH   # 5

TRANS_FLAG_POSITION      = 0                                           # 0, the index in send data char array
DATA_TYPE_POSITION       = TRANS_FLAG_POSITION + TRANS_FLAG_LENGTH     # 1, the index in send data char array
PARITY_POSITION          = DATA_TYPE_POSITION + DATA_TYPE_LENGTH       # 2, the index in send data char array
DATA_LEN_POSITION        = PARITY_POSITION + PARITY_LENGTH             # 3
DATA_POSITION            = DATA_LEN_POSITION + DATA_LEN_FLAG_LENGTH    # 5


# data type: float, double
DATA_FLOAT32             = 32
DATA_FLOAT64             = 64
DATA_BOOL                = 1
DATA_CHAR                = 8
DATA_UCHAR               = 9
DATA_INT                 = 32 + 1
DATA_LONG                = 64 + 1

# send data flag: 0~127
CONNECTION_FLAG          = 1
DATA_FLAG                = 2
EPISODE_START_FLAG       = 3
EPISODE_END_FLAG         = 4
TERMINATION_FLAG         = 5
CONTROL_FLAG             = 6
SUCCESS_RESPONSE_FLAG    = 7
ERROR_RESPONSE_FLAG      = 8

EVEN_FLAG                = 0
ODD_FLAG                 = 1

BUFFSIZE                 = 2048   # 255 double data, 510 float data


class Data_transfer(Number_conver, Tcpsocket):
    def __init__(self, conn_type='server', port_num=8088, buffsize=200, host='127.0.0.1', debug_print=True):
        Tcpsocket.__init__(self, conn_type, port_num, buffsize, host, debug_print)
        Number_conver.__init__(self, debug_print)

    def parity_check(self, data):
        parity_num = 0
        lens = len(data)
        for i in range(lens):
            parity_num += (data[i] % 2)
        if parity_num % 2:
            return ODD_FLAG          # odd
        return EVEN_FLAG             # even

    # when linux send char, the negative num send with the format of Complement:
    def recv_char2byte(self, input_data):
        output_data = []
        for i in range(len(input_data)):
            temp_bin = self.byte2bin(input_data[i])
            if temp_bin[0] == 1:
                temp_bin[0] = 0
                abs_data = self.bin2byte(temp_bin) - 1
                temp_bin = self.byte2bin(127 - abs_data)
                temp_bin[0] = 1
                output_data.append(self.bin2byte(temp_bin))
            else:
                output_data.append(input_data[i])
        return output_data

    # trans float data list to the format of send byte
    # data format: 0: data_flag;1: data_type;2: parity_flag;3: data_length high;
    # 4: data_length low;5~: byte data
    def float2send_byte(self, float_data, bit=32, send_type='data'):
        if bit != 32 and bit != 64:
            raise Exception("float bit choose error !")

        data_bys = self.float_array2bys(float_data, bit)
        self.debug_print("data_bys", data_bys, len(data_bys))
        parity_flag = self.parity_check(data_bys)
        data_length = len(float_data)

        send_bys = []
        # add send_flag:
        if send_type == 'data':
            send_bys.append(DATA_FLAG)
        elif send_type == 'control':
            send_bys.append(CONTROL_FLAG)
        else:
            raise Exception("send type error !")

        # add data_type:
        if bit == 32:
            send_bys.append(DATA_FLOAT32)
        else:
            send_bys.append(DATA_FLOAT64)
        # add parity flag:
        send_bys.append(parity_flag)
        # add data length's high byte:
        send_bys.append(data_length // 256)
        # add data length's low byte:
        send_bys.append(data_length % 256)
        # add data:
        for i in range(len(data_bys)):
            send_bys.append(data_bys[i])
        return send_bys

    # trans control instructions to the format of send byte
    # data format: 0: send_flag(control flag); 1: module_name length; 2: func_name length;
    # 3: parameters nums; 4: data length
    # module name, func_name, [param data type, param_data]...
    # data_lens: len(module_name) + len(func_name) + parameters nums + parameters bytes
    def instruc2send_byte(self, module_name, func_name, params_list):
        module_name_lens = len(module_name)
        func_name_lens = len(func_name)
        param_lens = len(params_list)

        int_module_name = [ord(module_name[i]) for i in range(module_name_lens)]
        int_func_name = [ord(func_name[i]) for i in range(func_name_lens)]
        self.debug_print("module_name", int_module_name, module_name_lens)
        self.debug_print("func_name", int_func_name, func_name_lens)
        data_lens = module_name_lens + func_name_lens + param_lens
        for i in range(param_lens):
            data_lens += int(params_list[i][0] / 8)
        send_bys = []

        # 0. add send_flag:
        send_bys.append(CONTROL_FLAG)
        # 1. add module_name lengths:
        send_bys.append(module_name_lens)
        # 2. add func_name lengths:
        send_bys.append(func_name_lens)
        # 3. add parameters nums:
        send_bys.append(param_lens)
        # 4. add data_lens:
        send_bys.append(data_lens)
        # add module_name:
        for i in range(module_name_lens):
            send_bys.append(int_module_name[i])
        # add func_name:
        for i in range(func_name_lens):
            send_bys.append(int_func_name[i])

        # add params_list:
        for i in range(param_lens):
            data_type = params_list[i][0]  # float or double
            parameters = params_list[i][1]
            # add parameter data type:
            send_bys.append(params_list[i][0])
            # add parameter data:
            param_bys = self.float2byte(parameters, data_type)
            for i in range(len(param_bys)):
                send_bys.append(param_bys[i])
        return send_bys

    # trans received byte to float data list
    def recv_byte2float(self, recv_bys):
        data_type = ord(recv_bys[DATA_TYPE_POSITION])  # 32 or 64
        parity_flag = ord(recv_bys[PARITY_POSITION])
        data_length = ord(recv_bys[DATA_LEN_POSITION]) * 256 + ord(recv_bys[DATA_LEN_POSITION + 1])
        data_list = recv_bys[DATA_POSITION:(DATA_POSITION + data_length * int(data_type / 8))]
        data_bys = [ord(v) for v in data_list]
        if parity_flag != self.parity_check(data_bys):
            print("parity check error !")
        float_array = self.bys2float_array(data_bys, data_type)
        return float_array, data_type

    def send_flag(self, flag):
        # send_bys = bytes([flag])
        send_bys = chr(flag)
        self.debug_print("send_flag", send_bys, len(send_bys))
        self.send_bytes(send_bys)

    def send_data(self, float_array, bit=32, send_type='data'):  # send_type: 'data' or 'control'
        send_list = self.float2send_byte(float_array, bit, send_type)
        send_bys = ''
        for i in range(len(send_list)):
            send_bys += chr(send_list[i])
        # print("send bys: ", send_bys)
        self.debug_print("send_bys", send_bys, len(send_bys))
        self.send_bytes(send_bys)

    # func_name: strings, params_list: [[data_type, data]... ]
    def send_control_instruction(self, module_name, func_name, params_list):
        send_list = self.instruc2send_byte(module_name, func_name, params_list)
        send_bys = ''
        for i in range(len(send_list)):
            send_bys += chr(send_list[i])
        self.debug_print("send_bys", send_bys, len(send_bys))
        self.send_bytes(send_bys)

    def recv_data(self, recv_lens=0):
        float_array = []
        recv_char = self.recv_bytes(recv_lens)
        # print(type(recv_char), recv_char[0], len(recv_char), type(ord(recv_char[0])))
        recv_bys = []
        for i in range(len(recv_char)):
            recv_bys.append(recv_char[i])
        self.debug_print("recv_bys", recv_bys, len(recv_bys))
        # print(recv_bys)

        recv_flag = ord(recv_bys[TRANS_FLAG_POSITION])
        if DATA_FLAG == recv_flag or CONTROL_FLAG == recv_flag:
            data_type = ord(recv_bys[DATA_TYPE_POSITION])  # 32 or 64
            data_length = ord(recv_bys[DATA_LEN_POSITION]) * 256 + ord(recv_bys[DATA_LEN_POSITION + 1])
            all_lens = 5 + data_length * int(data_type / 8)
            received_lens = len(recv_bys)
            rest_lens = all_lens - received_lens

            while rest_lens:
                recv_char = self.recv_bytes(rest_lens)
                temp_bys = self.recv_char2byte(recv_char)
                for i in range(len(temp_bys)):
                    recv_bys.append(temp_bys[i])
                rest_lens -= len(temp_bys)
            float_array, _ = self.recv_byte2float(recv_bys)

        # recv_flag = int(recv_bys[TRANS_FLAG_POSITION])
        # if DATA_FLAG == recv_flag or CONTROL_FLAG == recv_flag:
        #     data_type = int(recv_bys[DATA_TYPE_POSITION])  # 32 or 64
        #     data_length = int(recv_bys[DATA_LEN_POSITION]) * 256 + int(recv_bys[DATA_LEN_POSITION + 1])
        #     all_lens = 5 + data_length * int(data_type / 8)
        #     received_lens = len(recv_bys)
        #     rest_lens = all_lens - received_lens
        #
        #     while rest_lens:
        #         recv_char = self.recv_bytes(rest_lens)
        #         temp_bys = self.recv_char2byte(recv_char)
        #         for i in range(len(temp_bys)):
        #             recv_bys.append(temp_bys[i])
        #         rest_lens -= len(temp_bys)
        #     float_array, _ = self.recv_byte2float(recv_bys)
        return recv_flag, float_array

    def terminate(self):
        print("send termination flag to hexa !")
        self.send_flag(TERMINATION_FLAG)
        self.close_socket()

    def handshake(self):
        if self.conn_type == 'server':
            print("waiting for connection flag...")
            recv_flag, _ = self.recv_data()
            if CONNECTION_FLAG != recv_flag:
                print("connect with client error !")
                return
            else:
                print("connect with client success !")
        elif self.conn_type == 'client':
            print("send connection flag...")
            self.send_flag(CONNECTION_FLAG)
            print("handshake success !")
