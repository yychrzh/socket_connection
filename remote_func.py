from hexabody import hexa, hexa_body, hexa_head, hexa_leg, hexa_legs
from py_protocol import Data_transfer

# send data flag: 0~127
CONNECTION_FLAG          = 1
DATA_FLAG                = 2
EPISODE_START_FLAG       = 3
EPISODE_END_FLAG         = 4
TERMINATION_FLAG         = 5
CONTROL_FLAG             = 6
RESPONSE_FLAG            = 7


class remote_func(Data_transfer, hexa):
    def __init__(self, conn_type='server', port_num=8088, buffsize=200, host='127.0.0.1', debug_print=True):
        Data_transfer.__init__(self, conn_type, port_num, buffsize, host, debug_print)
        hexa.__init__(self)

    # Available returns whether driver is available or not.
    def Available(self):
        self.send_control_instruction("Available", [])
        # waiting for response !
        recv_flag, recv_array = self.recv_data()  # 1 float (bool)
        if recv_flag == DATA_FLAG and len(recv_array) > 0:
            return int(recv_array[0])
        else:
            # print("didn't receive response whrn run Available func !")
            return -1

    # Start starts the hexabody driver.
    def Start(self):
        return

    # RotationDirection returns the direction of rotation, 1 means clockwise, -1 means anticlockwise.
    def RotationDirection(self):
        return

    # Releax reduces power to all servos on HEXA to save battery.
    def Relax(self):
        return

    # Close shuts down the hexabody driver.
    def Close(self):
        return