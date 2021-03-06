#-*-coding:utf-8-*-
import time
from data_transfer.py_protocol import Data_transfer
from hexapod.remote_robot import Hexa, HexaBody, HexaHead, HexaLeg

# send data flag: 0~127
CONNECTION_FLAG          = 1
DATA_FLAG                = 2
EPISODE_START_FLAG       = 3
EPISODE_END_FLAG         = 4
TERMINATION_FLAG         = 5
CONTROL_FLAG             = 6
SUCCESS_RESPONSE_FLAG    = 7
ERROR_RESPONSE_FLAG      = 8

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
        # conn.send_control_instruction("start", [[DATA_FLOAT64, 1.90],
        # [DATA_FLOAT32, -0.123], [DATA_FLOAT64, 1112]])
        conn.send_control_instruction(func_name_list[count], param_list[count])

        print("send success, waiting for response !")
        recv_flag, recv_array = conn.recv_data()
        print(recv_flag, recv_array)
        count += 1
        if count == len(func_name_list):
            conn.send_flag(TERMINATION_FLAG)
            conn.close_socket()
            break


def remote_control1(hexa):
    hexabody_driver = hexa.Available()
    print("Is hexabody's driver available ? ", hexabody_driver)

    hexabody_start = hexa.Start()
    print("Is hexabody start ? ", hexabody_start)

    # hexabody_r_dir = hexa.RotationDirection()
    # print("hexabody's RotationDirection: %d" % hexabody_r_dir)

    hexabody_relax = hexa.Relax()
    print("Is hexabody Relax ? ", hexabody_relax)

    hexabody_close = hexa.Close()
    print("Is hexabody Close ? ", hexabody_close)

    hexabody_driver = hexa.Available()
    print("Is hexabody's driver available ? ", hexabody_driver)

    hexa.terminate()
    return


def remote_control2(conn, hexabody):
    hexabody_driver = hexabody.Available()
    print("Is hexabody's driver available ? ", hexabody_driver)

    hexabody_start = hexabody.Start()
    print("Is hexabody start ? ", hexabody_start)

    # test
    hexabody.Stand()
    time.sleep(1)
    hexabody.Lift(-10)
    time.sleep(1)
    hexabody.Lift(30)
    time.sleep(1)
    hexabody.Stand()
    time.sleep(1)
    hexabody.Pitch(10, 100)
    time.sleep(1)
    hexabody.StopPitch()
    time.sleep(1)
    hexabody.Spin(60, 100)
    time.sleep(1)
    hexabody.Stand()

    hexabody_relax = hexabody.Relax()
    print("Is hexabody Relax ? ", hexabody_relax)

    hexabody_close = hexabody.Close()
    print("Is hexabody Close ? ", hexabody_close)

    hexabody_driver = hexabody.Available()
    print("Is hexabody's driver available ? ", hexabody_driver)

    conn.terminate()
    return


def remote_control(conn):
    hexa = Hexa(conn)
    hexabody = HexaBody(conn)
    hexahead = HexaHead(conn)
    hexaleg = HexaLeg(conn)


if __name__ == "__main__":
    print("create socket server, waiting to connect to hexa robot...")
    conn = Data_transfer('server', hexa_port_num, buffsize=2048,
                         debug_print=False)
    conn.handshake()
    remote_control(conn)


