from data_transfer.py_protocol import *


def create_conn(name, conn_type='server', port_num=8088, buffsize=200, host='127.0.0.1', debug_print=False):
    print("create socket connection:", name)
    conn = Data_transfer(conn_type, port_num, buffsize, host, debug_print)
    print("conn handshake:")
    conn.handshake()
    return conn


def data_trans(conn, data):   # data: float data list:
    conn.send_data(data, bit=64)
    recv_flag, _ = conn.recv_data()
    if SUCCESS_RESPONSE_FLAG == recv_flag:
        print("data sent success !")
    elif ERROR_RESPONSE_FLAG == recv_flag:
        print("data sent error !")
    elif TERMINATION_FLAG == recv_flag:
        print("receive terminate flag, close conn !")
        conn.close_socket()


# send position info after robot's request
def robot_request(name, camera, conn_type='server', port_num=8088,
                  buffsize=200, host='127.0.0.1', debug_print=False):
    conn = create_conn(name, conn_type, port_num, buffsize, host, debug_print)
    while True:
        print("camera waiting data from robot...")
        recv_flag, _ = conn.recv_data()
        # print("camera receive flag: ", recv_flag)

        if CONNECTION_FLAG == recv_flag:
            print("receive data flag, send current position info to robot !")
            pos_data = [camera.robot_x, camera.robot_y,
                        camera.charge_x, camera.charge_y]
            conn.send_data(pos_data, bit=64)
            recv_flag, _ = conn.recv_data()
            if recv_flag != SUCCESS_RESPONSE_FLAG:
                print("receive error response from robot !")
        elif TERMINATION_FLAG == recv_flag:
            print("receive terminate flag, close conn !")
            conn.close_socket()


# send position info to robot and wait for response
def robot_response(name, camera, conn_type='server', port_num=8088,
                   buffsize=200, host='127.0.0.1', debug_print=False):
    conn = create_conn(name, conn_type, port_num, buffsize, host, debug_print)
    while True:
        pos_data = [camera.robot_x, camera.robot_y,
                    camera.charge_x, camera.charge_y]
        conn.send_data(pos_data, bit=64)
        recv_flag, _ = conn.recv_data()

        if SUCCESS_RESPONSE_FLAG == recv_flag:
            print("data sent success !")
        elif ERROR_RESPONSE_FLAG == recv_flag:
            print("data sent error !")
        elif TERMINATION_FLAG == recv_flag:
            print("receive terminate flag, close conn !")
            conn.close_socket()


class Camera(object):
    def __init__(self):
        self.robot_x = 0.1
        self.robot_y = 0.2
        self.charge_x = 1.0
        self.charge_y = 1.2


