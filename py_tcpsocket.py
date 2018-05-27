#-*-coding:utf-8-*-
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
        self.conn_type = conn_type
        if self.conn_type == 'server':
            self.conn = self.create_connect_server()
        elif self.conn_type == 'client':
            self.conn = self.create_connect_client()
        else:
            print("socket type wrong !")

    # print debug strings if needed
    def debug_print(self, info):
        if self.debug_print_flag:
            print("(tcp " + self.conn_type + ")", info)

    # create the socket server connection
    def create_connect_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', self.port_num))
        server.listen(5)
        conn, address = server.accept()
        self.debug_print("accept from client " + str(address) + " success !")
        return conn

    # create the socket client connection
    def create_connect_client(self):
        addr = (self.host, self.port_num)
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(addr)
        self.debug_print("connect with server " + self.host + ":" + str(self.port_num) + " success !")
        return conn

    # send data with the format of strings
    def send_strings(self, send_str):
        real_send_lens = self.conn.send(bytes("%s" % send_str, encoding="ascii"))
        if real_send_lens < len(send_str):
            self.debug_print("not all data has been sent")

    # receive data with the format of strings, no bigger than self.BUFFSIZE bytes
    def recv_strings(self):
        recv_str = self.conn.recv(self.BUFFSIZE)
        if recv_str == b'':
            self.debug_print("the connection might have broken !")
        recv_str = recv_str.decode("ascii")
        return recv_str

    def recv_bytes(self):
        recv_str = self.conn.recv(self.BUFFSIZE)
        if recv_str is b'':
            self.debug_print("the connection might have broken !")
        return recv_str

    def close_socket(self):
        if self.conn_type == 'client':
            self.debug_print("shutdown and close socket connection !")
            self.conn.shutdown(2)
            self.conn.close()