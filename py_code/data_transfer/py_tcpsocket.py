#-*-coding:utf-8-*-
import socket


# tcp socket, send and receive strings


class Tcpsocket(object):
    def __init__(self, conn_type='server', port_num=8088, buffsize=200, host='127.0.0.1', debug_print=True):
        self.host = host
        self.port_num = port_num
        self.BUFFSIZE = buffsize
        self.debug_print_flag = debug_print
        self.conn_type = conn_type
        if self.conn_type == 'server':
            self.conn = self.create_connect_server()
        elif self.conn_type == 'client':
            self.conn = self.create_connect_client()
        else:
            print("socket type wrong !")

    # print debug strings if needed
    def t_debug_print(self, info):
        if self.debug_print_flag:
            print("(tcp " + self.conn_type + ")", info)

    # create the socket server connection
    def create_connect_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', self.port_num))
        server.listen(5)
        conn, address = server.accept()
        # self.t_debug_print("accept from client " + str(address) + " success !")
        print("accept from client " + str(address) + " success !")
        return conn

    # create the socket client connection
    def create_connect_client(self):
        addr = (self.host, self.port_num)
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(addr)
        # self.t_debug_print("connect with server " + self.host + ":" + str(self.port_num) + " success !")
        print("connect with server " + self.host + ":" + str(self.port_num) + " success !")
        return conn

    # send data with the format of strings
    def send_strings(self, send_str):
        real_send_lens = self.conn.send(bytes("%s" % send_str, encoding="ascii"))
        if real_send_lens < len(send_str):
            self.t_debug_print("not all data has been sent")

    # receive data with the format of strings, no bigger than self.BUFFSIZE bytes
    def recv_strings(self):
        recv_str = self.conn.recv(self.BUFFSIZE)
        if recv_str == b'':
            self.t_debug_print("the connection might have broken !")
        recv_str = recv_str.decode("ascii")
        return recv_str

    def send_bytes(self, send_bytes):
        real_send_lens = self.conn.send(send_bytes)
        if real_send_lens < len(send_bytes):
            self.t_debug_print("not all data has been sent")

    def recv_bytes(self, recv_lens=0):
        if recv_lens == 0:
            recv_b = self.conn.recv(self.BUFFSIZE)
            # print("conn.recv: ", recv_b)
        else:
            recv_b = self.conn.recv(recv_lens)
        if recv_b == b'':
            print("the connection might have broken !")
            # recv_b = self.conn.recv(self.BUFFSIZE)
            # print(recv_b)
        return recv_b

    def close_socket(self):
        if self.conn_type == 'client':
            print("shutdown and close socket connection !")
            self.conn.shutdown(2)
            self.conn.close()