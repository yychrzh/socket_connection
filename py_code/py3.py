from data_transfer.py_protocol import *
import random
import time


def float_test(conn):
    while True:
        recv_flag, recv_array = conn.recv_data()
        if DATA_FLAG == recv_flag:
            conn.send_data(recv_array, 64)
        elif TERMINATION_FLAG == recv_flag:
            conn.close_socket()
            break


if __name__ == '__main__':
    print("create socket server, waiting to connect to hexa robot...")
    conn = Data_transfer('client', 4096, 2048, '127.0.0.1', False)
    conn.handshake()
    # conn.send_flag(CONNECTION_FLAG)
    # recv_flag, recv_data = conn.recv_data()
    # print("recv_flag, recv_data: ", recv_flag, recv_data)
    # conn.send_flag(TERMINATION_FLAG)
    # conn.close_socket()
    float_test(conn)