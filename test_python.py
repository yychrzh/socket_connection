#-*-coding:utf-8-*-
from py_tcpsocket import tcpsocket
import time
from number_conversion import *


def read_one_line_from_screen():
    recv_str = input()
    return recv_str


def server_test(conn):
    while True:
        recv_str = conn.recv_strings()
        if recv_str == "":
            break
        print("receive from client: ", recv_str)
        print("receive data lens: %d" % len(recv_str))
        time.sleep(0.05)
        conn.send_strings(recv_str)


def client_test(conn):
    test_times = 0
    while True:
        test_times += 1
        print("please input one line data:")
        send_str = read_one_line_from_screen()
        conn.send_strings(send_str)
        print("send data lens: %d" % len(send_str))
        recv_str = conn.recv_strings()
        if recv_str == "":
            break
        print("receive from server: ", recv_str)
        time.sleep(0.05)
        if test_times > 1:
            conn.close_socket()


# test in server mode:
def byte_test(conn):
    recv_bytes = conn.recv_bytes()
    print("recv_bytes: ", recv_bytes)
    print("recv_lens: ", len(recv_bytes))
    print("recv type: ", type(recv_bytes))
    int_bytes = [int(v) for v in recv_bytes]
    for i in range(len(int_bytes)):
        int_bytes[i] = byte2char(int_bytes[i])
    print("recv_int: ", int_bytes)
    send_bytes = bytes([0, 64, 127, 192, 255, 128])
    conn.send_bytes(send_bytes)


if __name__ == "__main__":
    port_num = 8088
    socket_type = 'server'
    print("please input socket port num(default: 8088, >2048):")
    recv_str = read_one_line_from_screen()
    if recv_str != "":
        if int(recv_str) > 2048:
            port_num = int(recv_str)

    print("please input socket type(server or client):")
    recv_str = read_one_line_from_screen()
    socket_type = recv_str
    if socket_type == 'server':
        print("create socket server, waiting for client:")
        conn = tcpsocket(conn_type=socket_type, port_num=port_num, buffsize=200, debug_print=True)
        # server_test(conn)
        byte_test(conn)
    elif socket_type == 'client':
        print("create socket client, please input server ip(default: '127.0.0.1'):")
        recv_str = read_one_line_from_screen()
        conn = tcpsocket(conn_type=socket_type, port_num=port_num, buffsize=200, host=recv_str, debug_print=True)
        client_test(conn)
    else:
        print("socket type input error !")
