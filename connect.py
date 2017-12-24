import socket
import os
import time
import math

HOST = '127.0.0.1'

class socket_conn(object):
    def __init__(self, conn_type=0, host='127.0.0.1', port_num=8088, bufsize=200):
        self.debug_flag = False

        self.host = host
        self.port_num = port_num
        self.BUFSIZE = bufsize

        # data: data_flag:0~6 + parity_flag:7 + data_len_flag:8 + data:~(no more than 127)
        self.data_width = 4
        self.MAX_SEND_DATA = 127

        self.min_one_bit_num = 1
        self.max_one_bit_num = 127
        self.data_one_bit_range = 127
        self.data_low_range = 1
        self.data_high_range = self.data_one_bit_range**self.data_width # (int)(self.data_one_bit_range * (1 - self.data_one_bit_range**self.data_width) / (1 - self.data_one_bit_range))

        self.connect_flag = "CONNECT"
        self.data_flag = "DATA   "
        self.episode_start_flag = "E_START"
        self.episode_end_flag = "E_END  "
        self.train_end_flag = "T_END  "

        self.flag_length = 7
        self.parity_length = 1
        self.data_len_flag_length = 1

        self.parity_position = self.flag_length
        self.data_len_position = self.parity_position + self.parity_length
        self.data_position = self.data_len_position + self.data_len_flag_length

        # create socket server
        if conn_type == 0:
            self.conn = self.create_connect_server()
            self.recv_connect_flag()
        else:
            self.conn = self.create_connect_client()
            self.send_connect_flag()

        # test the connecting with the client
        # self.connect_test()

    # create the socket connection and recv the connect_flag from the client
    def create_connect_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', self.port_num))
        server.listen(0)
        conn, address = server.accept()
        print(conn, address)
        return conn

    def recv_connect_flag(self):
        recv_flag, recv_data = self.recv()
        if recv_flag == self.connect_flag:
            print("connect with client success")
            time.sleep(0.1)

    def create_connect_client(self):
        addr = (self.host, self.port_num)
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(addr)
        return conn

    def send_connect_flag(self):
        time.sleep(0.1)
        print("send connect flag")
        self.send(self.connect_flag)
        # time.sleep(0.5)

    # recv from the client and judge the recv_flag: recv data range: [1, 127]
    def recv(self):
        if self.debug_flag:
            print("waiting for client data...")
        recv_str = self.recv_ascii()                      # recv the ascii data
        recv_flag = self.recv_flag(recv_str)              # recv the recv_flag
        recv_list = self.recv_byte(recv_str)              # trans the ascii data to byte data
        recv_data = []
        if recv_flag == self.data_flag:
            if self.debug_flag:
                print("recv recv_flag:")
            recv_data = self.recv_data(recv_list)
            if self.debug_flag:
                print("recv_data: ", recv_data)
        return recv_flag, recv_data

    # send data or flag to the client
    def send(self, send_flag, data=None):
        if send_flag == self.data_flag:
            if data is None:
                print("error: data is none")
            else:
                if self.debug_flag:
                    print("send data to client:")
                self.send_data(data)
                if self.debug_flag:
                    print("send_data: ", data)
        else:
            self.send_flag(send_flag)

    # recv the ascii data
    def recv_ascii(self):
        recv_str = self.conn.recv(self.BUFSIZE)
        recv_str = recv_str.decode("ascii")
        if self.debug_flag:
            print("success recv data string: ", recv_str)
        return recv_str

    # trans the ascii data to byte data
    def recv_byte(self, recv_str):
        recv_list = []
        for i in range(len(recv_str)):
            temp = ord(recv_str[i])
            recv_list.append(temp)
        if self.debug_flag:
            print("recv recv_list: ", recv_list)
        return recv_list

    def recv_data(self, recv_list):
        byte_data = recv_list[self.data_position:]
        byte_data_lens = len(byte_data)
        # check the parity flag
        parity_flag = recv_list[self.parity_position]
        if (parity_flag - 1) != self.parity_check(byte_data):
            print("error: parity error, data is wrong")

        # check the data len flag
        data_lens = recv_list[self.data_len_position]
        if data_lens != byte_data_lens / self.data_width:
            print("error: data lens error, data is wrong")
        recv_data = self.byte_data_trans(byte_data)  # remove the data_flag and data_length_flag
        return recv_data

    # remove the data_flag and data_length_flag
    def remove_flag(self, recv_list):
        data_lens = recv_list[self.data_len_position]
        data = []
        for i in range(data_lens):
            data.append(recv_list[self.data_len_position + 1 + i])
        return data

    # return the recv_flag
    def recv_flag(self, recv_str):
        if self.debug_flag:
            print("recv recv_flag: ", recv_str[0:self.flag_length])
        return recv_str[0:self.flag_length]

    # input: data range: float [-1, 1] vector
    def send_data(self, input):
        data = self.float_data_trans(input)   #data lens : len(input) * self.data_width
        send_str = self.send_str_gen(data)
        self.conn.send(bytes("%s" % send_str, encoding="ascii"))

    # generate the send string
    def send_str_gen(self, data):
        data_lens = len(data)
        if data_lens > self.MAX_SEND_DATA * self.data_width:
            print("error: data length is too long")
        dstr = []
        parity_flag = self.parity_check(data) + 1                     # get parity flag
        dstr.append(self.data_flag)                                   # add data flag
        dstr.append(chr(parity_flag))                                 # add parity flag
        dstr.append(chr((int)(data_lens/self.data_width)))            # add data length flag to send_data
        for i in range(data_lens):
            temp = int(data[i])
            dstr.append(chr(temp))
        send_str = "".join(dstr)
        return send_str

    def send_flag(self, send_flag):
        send_str = send_flag
        self.conn.send(bytes("%s" % send_str, encoding="ascii"))

    # trans byte data [1, 127] to float data [-1, 1]
    def byte_data_trans(self, data):
        if self.debug_flag:
            print("trans byte data to float：")
            print("input: ", data)
        lens = int(len(data) / self.data_width)
        input = self.data_copy(data)
        output = []
        for i in range(lens):
            temp = 1
            for j in range(self.data_width):
                temp += (input[i*self.data_width+j] - 1) * (self.data_one_bit_range**j)
            output.append((float)(temp - 1) / (self.data_high_range -1) * 2 - 1)
        if self.debug_flag:
            print("ouput: ", output)
        return output

    # trans float data [-1, 1] to byte data [1, 127]
    def float_data_trans(self, data):
        lens = len(data)
        input = self.data_copy(data)
        if self.debug_flag:
            print("trans float data to byte：")
            print("input: ", input)
        output = []
        for i in range(lens):
            temp = (int)((input[i] + 1) / 2 * (self.data_high_range -1) + 1)
            for j in range(self.data_width):
                div = (temp-1) / self.data_one_bit_range
                rem = (temp-1) % self.data_one_bit_range
                temp = div+1
                output.append((int)(rem+1))
        if self.debug_flag:
            print("ouput: ", output)
        return output

    def parity_check(self, data):
        parity_num = 0
        lens = len(data)
        for i in range(lens):
            parity_num += (data[i] % 2)
        if parity_num % 2:
            return 1         # odd

        return 0         # even

    def data_copy(self, data):
        lens = len(data)
        output = []
        for i in range(lens):
            output.append(data[i])
        return output

    def connect_close(self):
        self.conn.close()

    def connect_test(self):
        # send_data
        #data = [1, 56, 64, 87, 127]
        data = [-1, -0.125, 0, 0.37, 1]
        print("send data to client")
        self.send(self.train_end_flag)

        # recv_data
        recv_flag, recv_data = self.recv()
        if recv_flag == self.data_flag:
            print(recv_data)
            
# the next code used the json and pickle to trans float data
import json

class socket_trans(object):
    def __init__(self, conn_type=0, host='127.0.0.1', port_num=8086, bufsize=1024):
        self.host = host
        self.port_num = port_num
        self.BUFSIZE = bufsize

        self.connect_flag =         [110]
        self.connect_success_flag = [111]
        self.data_flag =            [112]
        self.episode_start_flag =   [113]
        self.episode_end_flag =     [114]
        self.train_end_flag =       [115]

        if conn_type == 0:
            self.conn = self.create_connect_server()
        else:
            self.conn = self.create_connect_client()

    def create_connect_server(self):
        address = ('', self.port_num)
        tcpSrvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpSrvSock.bind(address)
        tcpSrvSock.listen(5)
        conn, addr = tcpSrvSock.accept()
        print(conn, addr)
        return conn

    def create_connect_client(self):
        addr = (self.host, self.port_num)
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(addr)
        return conn

    def send(self, data):
        json_string = json.dumps(data)
        nameBytes = json_string.encode('utf-8')
        self.conn.send(nameBytes)
        # self.conn.send(json_string)

    def recv(self):
        json_string = self.conn.recv(self.BUFSIZE)
        nameStr = json_string.decode('utf-8')
        data = json.loads(nameStr)
        # data = json.loads(json_string)
        return data

    def connect_close(self):
        self.conn.close()


from multiprocessing.connection import Listener
from multiprocessing.connection import Client

# connection with multiprocessing.connection
# in order to trans between python2. and python3. ,
# you should revise the pickle protocol in the multiprocessing connection.py

class multi_connection(object):
    def __init__(self, conn_type=0, host='127.0.0.1', port_num=8086, bufsize=1024):
        self.host = host
        self.port_num = port_num
        self.BUFSIZE = bufsize

        self.connect_flag =         [110]
        self.connect_success_flag = [111]
        self.data_flag =            [112]
        self.episode_start_flag =   [113]
        self.episode_end_flag =     [114]
        self.train_end_flag =       [115]

        if conn_type == 0:
            self.conn = self.create_connect_server()
            self.recv_flag(self.connect_flag)
        else:
            self.conn = self.create_connect_client()
            self.send_flag(self.connect_flag)

    def create_connect_server(self):
        address = ('localhost', self.port_num)
        listener = Listener(address, authkey=b'secret password A')
        conn = listener.accept()
        return conn

    def create_connect_client(self):
        address = (self.host, self.port_num)
        conn = Client(address, authkey=b'secret password A')
        return conn

    def recv_flag(self, input_flag):
        recv_flag = self.conn.recv()
        if input_flag[0] == recv_flag[0]:
            print("recv flag success")
            # time.sleep(0.1)
        else:
            print("recv flag wrong!")

    def send_flag(self, input_flag):
        self.conn.send(input_flag)

    def recv(self):
        self.conn.recv()

    def send(self, data_list):
        self.conn.send(data_list)