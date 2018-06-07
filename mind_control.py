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
RESPONSE_FLAG            = 7

# data type: float, double
DATA_FLOAT32             = 32
DATA_FLOAT64             = 64
DATA_BOOL                = 1
DATA_CHAR                = 8
DATA_UCHAR               = 9
DATA_INT                 = 32 + 1
DATA_LONG                = 64 + 1

robot_ip = '192.168.123.111'  # '10.20.4.113'
hexa_port_num = 4096


# control with remote python:
def remote_test(conn):
    # recv connect flag:
    print("waiting for connection flag...")
    recv_flag, _ = conn.recv_data()
    if CONNECTION_FLAG != recv_flag:
        print("connect with client error !")
        return
    else:
        print("connect with client success !")

    func_name_list = ["available", "start", "relax", "close"]
    param_list = [
        [],
        [[DATA_FLOAT64, 1.08]],
        [[DATA_FLOAT32, -0.123], [DATA_FLOAT64, 1112]],
        []
    ]

    count = 0
    while True:
        # send one control instructions to robot
        # conn.send_data([1, 2, 3], 64, 'control')
        print("send one control instruction to robot !")
        # conn.send_control_instruction("start", [[DATA_FLOAT64, 1.90], [DATA_FLOAT32, -0.123], [DATA_FLOAT64, 1112]])
        conn.send_control_instruction(func_name_list[count], param_list[count])

        print("send success, waiting for response !")
        recv_flag, recv_array = conn.recv_data()
        print(recv_flag, recv_array)
        count += 1
        if count == len(func_name_list):
            conn.send_flag(TERMINATION_FLAG)
            conn.close_socket()
            break


def remote_control(conn):
    return


if __name__ == "__main__":
    print("create socket server, waiting to connect to hexa robot...")
    conn = Data_transfer('server', hexa_port_num, buffsize=2048, debug_print=False)
    remote_control(conn)


