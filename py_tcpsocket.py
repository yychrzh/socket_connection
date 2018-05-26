import socket
import os
import time
import math


# tcp socket, send and receive strings


class tcpsocket(object):
    def __init__(self, conn_type='server', port_num=8088, buffsize=200, host='127.0.0.1', debug_print=True):
        self.host = host
        self.port_num = port_num
        self.BUFFSIZE = buffsize
        self.debug_print_flag = debug_print
        if conn_type == 'server':
            self.conn = self.create_connect_server()
        else:
            self.conn = self.create_connect_client()

    # print debug strings if needed
    def debug_print(self, info):
        if self.debug_print_flag:
            print("(debug)", info)

    # create the socket server connection
    def create_connect_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', self.port_num))
        server.listen(0)
        conn, address = server.accept()
        self.debug_print([conn, address])
        return conn

    # create the socket client connection
    def create_connect_client(self):
        addr = (self.host, self.port_num)
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(addr)
        self.debug_print("connect with address " + self.host + " success in port: %d" % self.port_num)
        return conn

    # send data with the format of strings
    def send_strings(self, send_str):
        self.conn.send(bytes("%s" % send_str, encoding="ascii"))

    # receive data with the format of strings, no bigger than self.BUFFSIZE bytes
    def recv_strings(self):
        recv_str = self.conn.recv(self.BUFFSIZE)
        return recv_str