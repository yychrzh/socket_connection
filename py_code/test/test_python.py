#-*-coding:utf-8-*-
import time
import random
# from py_tcpsocket import Tcpsocket
# from number_conversion import *
from data_transfer.py_protocol import Data_transfer

# send data flag: 0~127
CONNECTION_FLAG          = 1
DATA_FLAG                = 2
EPISODE_START_FLAG       = 3
EPISODE_END_FLAG         = 4
TERMINATION_FLAG         = 5


def read_one_line_from_screen():
    recv_str = input()
    return recv_str


# test in mode server
def float_test(conn):
    MAX_COUNT = 100
    count = 0
    error_count = 0
    total_lens = 0

    # recv connect flag:
    print("waiting for connection flag...")
    recv_flag, _ = conn.recv_data()
    if CONNECTION_FLAG != recv_flag:
        print("connect with client error !")
        return
    else:
        print("connect with client success !")

    start_time = time.time()
    while True:
        send_array = []
        data_lens = random.randint(50, 250)
        for i in range(data_lens):
            send_array.append(random.uniform(-1e5, 1e5))  # produce 50 random float numbers

        print("send double data to client: ")
        # print(send_array)
        conn.send_data(send_array, bit=64)

        # time.sleep(0.05)

        print("data sent success, waiting for response !")
        recv_flag, recv_array = conn.recv_data()

        if DATA_FLAG == recv_flag:
            for i in range(data_lens):
                if recv_array[i] != send_array[i]:
                    print("error emerged in %d 's recv in the %d 's data, expect %.15f, but received %.15f"
                          % (count, i, send_array[i], recv_array[i]))
                    error_count += 1
                    break
            if error_count > 0:
                break

        current_time = time.time() - start_time
        print(">>>count: %3d, current_time: %.15f sec" % (count, current_time))
        count += 1
        total_lens += data_lens

        if MAX_COUNT == count:
            conn.send_flag(TERMINATION_FLAG)
            print("data transmission end, with %d data transfered error in total %d data"
                  % (error_count, total_lens))
            break


def agent_test():
    conn = Data_transfer('client', 5096, 2048, '10.20.4.35', debug_print=False)

    # recv connect flag:
    print("send connection flag...")
    conn.send_flag(CONNECTION_FLAG)

    # recv start flag:
    print("waiting for start flag...")
    recv_flag, _ = conn.recv_data()
    if EPISODE_START_FLAG != recv_flag:
        print("start error !")
        return
    else:
        print("start success !")

    MAX_COUNT = 10
    count = 0
    error_count = 0
    total_lens = 0
    start_time = time.time()
    while True:
        send_array = []
        data_lens = random.randint(50, 250)
        for i in range(data_lens):
            send_array.append(random.uniform(-1e5, 1e5))  # produce 50 random float numbers

        print("send double data to client: ")
        # print(send_array)
        conn.send_data(send_array, bit=64)

        # time.sleep(0.05)

        print("data sent success, waiting for response !")
        recv_flag, recv_array = conn.recv_data()

        if DATA_FLAG == recv_flag:
            for i in range(data_lens):
                if recv_array[i] != send_array[i]:
                    print("error emerged in %d 's recv in the %d 's data, expect %.15f, but received %.15f"
                          % (count, i, send_array[i], recv_array[i]))
                    error_count += 1
                    break
            if error_count > 0:
                break

        current_time = time.time() - start_time
        print(">>>count: %3d, current_time: %.15f sec" % (count, current_time))
        count += 1
        total_lens += data_lens

        if MAX_COUNT == count:
            conn.send_flag(TERMINATION_FLAG)
            print("data transmission end, with %d data transfered error in total %d data"
                  % (error_count, total_lens))
            conn.close_socket()
            break


if __name__ == "__main__":
    # agent_test()

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
        conn = Data_transfer(conn_type=socket_type, port_num=port_num, buffsize=2048, debug_print=True)
        # float_test(conn)
        conn.handshake()
    elif socket_type == 'client':
        print("create socket client, please input server ip(default: '127.0.0.1'):")
        recv_str = read_one_line_from_screen()
        conn = Data_transfer(conn_type=socket_type, port_num=port_num, buffsize=2048, host=recv_str, debug_print=False)
        conn.handshake()
    else:
        print("socket type input error !")

