from hexabody import hexa, hexa_body, hexa_head, hexa_leg, hexa_legs
from py_protocol import Data_transfer

# data type: float, double
DATA_FLOAT32             = 32
DATA_FLOAT64             = 64
DATA_BOOL                = 1
DATA_CHAR                = 8
DATA_UCHAR               = 9
DATA_INT                 = 32 + 1
DATA_LONG                = 64 + 1

# send data flag: 0~127
CONNECTION_FLAG          = 1
DATA_FLAG                = 2
EPISODE_START_FLAG       = 3
EPISODE_END_FLAG         = 4
TERMINATION_FLAG         = 5
CONTROL_FLAG             = 6
SUCCESS_RESPONSE_FLAG    = 7
ERROR_RESPONSE_FLAG      = 8

# GaitType
GaitOriginal = 0   # default gait
GaitWave     = 1   # 5+1 gait, 5 legs stay on the ground and 1 leg raise at the same time
GaitRipple   = 2   # 4+2 gait, 4 legs stay on the ground and 2 legs raise at the same time
GaitTripod   = 3   # 3+3 gait, 3 legs stay on the ground and 3 legs raise at the same time
GaitAmble    = 4   # 4+2 gait, 4 legs stay on the ground and 2 legs raise at the same time, different from GaitRipple.


class remote_hexa(Data_transfer, hexa, hexa_body):
    def __init__(self, conn_type='server', port_num=8088, buffsize=200, host='127.0.0.1', debug_print=True):
        Data_transfer.__init__(self, conn_type, port_num, buffsize, host, debug_print)
        hexa.__init__(self)
        hexa_body.__init__(self)

    def terminate(self):
        print("send termination flag to hexa !")
        self.send_flag(TERMINATION_FLAG)
        self.close_socket()

    def handshake(self):
        if self.conn_type == 'server':
            print("waiting for connection flag...")
            recv_flag, _ = self.recv_data()
            if CONNECTION_FLAG != recv_flag:
                print("connect with client error !")
                return
            else:
                print("connect with client success !")
        elif self.conn_type == 'client':
            print("send connection flag...")
            self.send_flag(CONNECTION_FLAG)

    def func_execute(self, func_name, param_list):
        self.send_control_instruction(func_name, param_list)
        # waiting for response !
        recv_flag, recv_array = self.recv_data()  # 1 float (bool)
        if recv_flag == DATA_FLAG:
            return recv_array
        elif recv_flag == SUCCESS_RESPONSE_FLAG or recv_flag == ERROR_RESPONSE_FLAG:
            return recv_flag
        else:
            print("didn't receive correct response when run %s func !" % func_name)
            return -1

    """*******************************************hexa************************************************"""
    # Available returns whether driver is available or not.
    def Available(self):  # return data: bool
        ret = self.func_execute("Available", [])[0]
        return ret

    # Start starts the hexabody driver.
    def Start(self):      # return data: error info
        ret = 1 if self.func_execute("Start", []) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # RotationDirection returns the direction of rotation, 1 means clockwise, -1 means anticlockwise.
    def RotationDirection(self):  # return data: -1 or 1
        ret = self.func_execute("RotationDirection", [])[0]
        return ret

    # Releax reduces power to all servos on HEXA to save battery.
    def Relax(self):
        ret = 1 if self.func_execute("Relax", []) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Close shuts down the hexabody driver.
    def Close(self):
        ret = 1 if self.func_execute("Close", []) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    """*******************************************hexa_body************************************************"""
    # Lift raises or reduces the height of HEXA's body in given height (-20 mm - 50 mm).
    def Lift(self, height):
        ret = 1 if self.func_execute("Lift", [[DATA_FLOAT64, height]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Pitch makes the body pitch at specified degree of angle in given duration.
    # The HEXA will pitch along the X axis of body coordinate.
    def Pitch(self, degree, duration):
        ret = 1 if self.func_execute("Pitch", [[DATA_FLOAT64, degree],
                                     [DATA_FLOAT64, duration]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # StopPitching stops an ongoing pitch.
    def StopPitch(self):
        ret = 1 if self.func_execute("StopPitch", []) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # PitchRoll returns LegPositions transformed from given pitchAngle and rollAngle degrees.
    def PitchRoll(self, pitchAngle, rollAngle):  # return LegPositions
        ret = self.func_execute("PitchRoll", [[DATA_FLOAT64, pitchAngle], [DATA_FLOAT64, rollAngle]])
        return ret

    # Stand makes the HEXA stand at the default height of 50mm.
    def Stand(self):
        ret = 1 if self.func_execute("Stand", []) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # StandWithHeight makes the HEXA stand with it's body at the specified height
    def StandWithHeight(self, height):
        ret = 1 if self.func_execute("StandWithHeight", [[DATA_FLOAT64, height]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # SelectGait chooses the walking gait of HEXA. 'SelectGaitWhileWalking' error will be returned
    # if the HEXA is walking. 'WrongGaitType' error will be returned if a wrong gait type is input.
    def SelectGait(self, gaitType):
        ret = 1 if self.func_execute("SelectGait", [[DATA_FLOAT64, gaitType]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # SetStepLength set the walking step length of HEXA. The range of stepLengthRatio is (0, 1].
    # 'OverflowStepLengthRatio' error will be returned if stepLengthRatio is out of its range.
    def SetStepLength(self, stepLengthRatio):
        ret = 1 if self.func_execute("SetStepLength", [[DATA_FLOAT64, stepLengthRatio]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Spin makes the HEXA use its legs to position itself in the given degree of rotation in given duration.
    def Spin(self, degree, duration):
        ret = 1 if self.func_execute("Spin", [[DATA_FLOAT64, degree],
                                              [DATA_FLOAT64, duration]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Marching is a kind of state of the walk. The leg of HEXA will be raised higher when it's walking.
    # It's different from the gait of the walk. StartMarching makes the HEXA enter the state of marching.
    def StartMarching(self):
        ret = 1 if self.func_execute("StartMarching", []) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # StopMarching makes the HEXA quit the state of marching.
    def StopMarching(self):
        ret = 1 if self.func_execute("StopMarching", []) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # WalkContinuously makes the HEXA walk continuously in given direction in degrees (0-359)
    # with given speed (0.1 cm/s - 1.2 cm/s). Call StopWalkingContinuously to stop.
    # 0 degrees is in the direction of the power button.
    # An increase in direction angle results in an anti-clockwise rotation.
    def WalkContinuously(self, direction, speed):
        ret = 1 if self.func_execute("WalkContinuously", [[DATA_FLOAT64, direction],
                                               [DATA_FLOAT64, speed]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # WalkingContinuously returns whether HEXA is walking continuously or not.
    def WalkingContinuously(self):
        ret = self.func_execute("WalkingContinuously", [])[0]
        return ret

    # StopWalkingContinuously stops the HEXA from walking continuously.
    def StopWalkingContinuously(self):
        ret = 1 if self.func_execute("StopWalkingContinuously", []) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Walk makes the HEXA walk one frame in given direction in degrees (0-359) with given duration.
    # Calling this function in a loop would give the same effect as calling WalkContinuously.
    # 0 degrees is in the direction of the power button. An increase in direction angle results in
    # an anti-clockwise rotation.
    def Walk(self, direction, duration):
        ret = 1 if self.func_execute("Walk", [[DATA_FLOAT64, direction],
                                              [DATA_FLOAT64, duration]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret