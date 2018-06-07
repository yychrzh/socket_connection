#-*-coding:utf-8-*-
import time
import random
from py_protocol import Data_transfer

# send data flag: 0~127
CONNECTION_FLAG          = 1
DATA_FLAG                = 2
EPISODE_START_FLAG       = 3
EPISODE_END_FLAG         = 4
TERMINATION_FLAG         = 5
CONTROL_FLAG             = 6

robot_ip = '192.168.123.111'  # '10.20.4.113'
hexa_port_num = 4096


# control with remote python:
def remote_control(conn):
    # recv connect flag:
    print("waiting for connection flag...")
    recv_flag, _ = conn.recv_data()
    if CONNECTION_FLAG != recv_flag:
        print("connect with client error !")
        return
    else:
        print("connect with client success !")

    while True:
        # send data or control instructions to robot
        conn.send_data([1, 2, 3], 64, 'control')

        recv_flag, recv_array = conn.recv_data()
        print(recv_flag, recv_array)
        conn.send_flag(TERMINATION_FLAG)
        conn.close_socket()
        break


if __name__ == "__main__":
    print("create socket server, waiting to connect to hexa robot...")
    conn = Data_transfer('server', hexa_port_num, buffsize=2048, debug_print=False)
    remote_control(conn)


