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


class func_execute(object):
    def __init__(self, conn, module_name):
        self.conn = conn
        self.module_name = module_name

    def __call__(self, func_name, param_list=None):
        if param_list is None:
            self.conn.send_control_instruction(self.module_name, func_name, [])
        else:
            self.conn.send_control_instruction(self.module_name, func_name, param_list)
        # waiting for response !
        recv_flag, recv_array = self.conn.recv_data()  # 1 float (bool)
        if recv_flag == DATA_FLAG:
            return recv_array
        elif recv_flag == SUCCESS_RESPONSE_FLAG or recv_flag == ERROR_RESPONSE_FLAG:
            return recv_flag
        else:
            print("didn't receive correct response when run %s func !" % func_name)
            return -1


class Hexa():
    def __init__(self, conn):
        self.conn = conn
        self.func_execute = func_execute(self.conn, "Hexa")

    # Available returns whether driver is available or not.
    def Available(self):  # return data: bool
        ret = self.func_execute("Available")[0]
        return ret

    # Start starts the hexabody driver.
    def Start(self):      # return data: error info
        ret = 1 if self.func_execute("Start") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Releax reduces power to all servos on HEXA to save battery.
    def Relax(self):
        ret = 1 if self.func_execute("Relax") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Close shuts down the hexabody driver.
    def Close(self):
        ret = 1 if self.func_execute("Close") == SUCCESS_RESPONSE_FLAG else 0
        return ret


class HexaBody():
    def __init__(self, conn):
        self.conn = conn
        self.func_execute = func_execute(self.conn, "Hexabody")

    # Lift raises or reduces the height of HEXA's body in given height (-20 mm - 50 mm).
    def Lift(self, height):
        ret = 1 if self.func_execute("Lift", [[DATA_FLOAT64,
                            height]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Pitch makes the body pitch at specified degree of angle in given duration.
    # The HEXA will pitch along the X axis of body coordinate.
    def Pitch(self, degree, duration):
        ret = 1 if self.func_execute("Pitch", [[DATA_FLOAT64, degree],
                            [DATA_FLOAT64, duration]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # StopPitching stops an ongoing pitch.
    def StopPitch(self):
        ret = 1 if self.func_execute("StopPitch") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Stand makes the HEXA stand at the default height of 50mm.
    def Stand(self):
        ret = 1 if self.func_execute("Stand") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # StandWithHeight makes the HEXA stand with it's body at the specified height
    def StandWithHeight(self, height):
        ret = 1 if self.func_execute("StandWithHeight",
                        [[DATA_FLOAT64, height]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # SelectGait chooses the walking gait of HEXA. 'SelectGaitWhileWalking' error will be returned
    # if the HEXA is walking. 'WrongGaitType' error will be returned if a wrong gait type is input.
    def SelectGait(self, gaitType):
        ret = 1 if self.func_execute("SelectGait", [[DATA_FLOAT64,
                        gaitType]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # SetStepLength set the walking step length of HEXA. The range of stepLengthRatio is (0, 1].
    # 'OverflowStepLengthRatio' error will be returned if stepLengthRatio is out of its range.
    def SetStepLength(self, stepLengthRatio):
        ret = 1 if self.func_execute("SetStepLength", [[DATA_FLOAT64,
                        stepLengthRatio]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Spin makes the HEXA use its legs to position itself in the given degree of rotation in given duration.
    def Spin(self, degree, duration):
        ret = 1 if self.func_execute("Spin", [[DATA_FLOAT64, degree],
                        [DATA_FLOAT64, duration]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Marching is a kind of state of the walk. The leg of HEXA will be raised higher when it's walking.
    # It's different from the gait of the walk. StartMarching makes the HEXA enter the state of marching.
    def StartMarching(self):
        ret = 1 if self.func_execute("StartMarching") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # StopMarching makes the HEXA quit the state of marching.
    def StopMarching(self):
        ret = 1 if self.func_execute("StopMarching") == SUCCESS_RESPONSE_FLAG else 0
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
        ret = self.func_execute("WalkingContinuously")[0]
        return ret

    # StopWalkingContinuously stops the HEXA from walking continuously.
    def StopWalkingContinuously(self):
        ret = 1 if self.func_execute("StopWalkingContinuously") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Walk makes the HEXA walk one frame in given direction in degrees (0-359) with given duration.
    # Calling this function in a loop would give the same effect as calling WalkContinuously.
    # 0 degrees is in the direction of the power button. An increase in direction angle results in
    # an anti-clockwise rotation.
    def Walk(self, direction, duration):
        ret = 1 if self.func_execute("Walk", [[DATA_FLOAT64, direction],
                        [DATA_FLOAT64, duration]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret


class HexaHead():
    def __init__(self, conn):
        self.conn = conn
        self.func_execute = func_execute(self.conn, "HexaHead")

    # Direction returns the current direction of HEXA's head in degrees (0-359).
    # 0 degrees is in the direction of the power button. The result is the degree
    # between the head and the power button in an anti-clockwise rotation.
    def Direction(self):
        ret = self.func_execute("Direction")[0]
        return ret

    # MoveHead moves the head to specified degree(0-359) in given duration.
    # 0 degrees is in the direction of the power button. An increase in direction
    # angle results in an anti-clockwise rotation.
    def MoveHead(self, degree, duration):
        ret = 1 if self.func_execute("MoveHead", [[DATA_FLOAT64, degree],
                        [DATA_FLOAT64, duration]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # RelaxHead reduces servo energy to head to save battery.
    def RelaxHead(self):
        ret = 1 if self.func_execute("RelaxHead") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # RotateHeadContinuously makes the head rotate continuously with specified
    # direction and speed (1 - 360).
    def RotateHeadContinuously(self, direction, speed):
        ret = 1 if self.func_execute("RotateHeadContinuously", [[DATA_FLOAT64, direction],
                        [DATA_FLOAT64, speed]]) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # RotatingHeadContinuously returns whether HEXA is rotating it's head continuously or not.
    def RotatingHeadContinuously(self):
        ret = self.func_execute("RotatingHeadContinuously")[0]
        return ret

    # StopRotatingHeadContinuously stops continuous rotation of the head.
    def StopRotatingHeadContinuously(self):
        ret = 1 if self.func_execute("StopRotatingHeadContinuously") == SUCCESS_RESPONSE_FLAG else 0
        return ret


"""
var JointDegreeRanges = []JointDegreeRange{
    JointDegreeRange{35, 145},
    JointDegreeRange{10, 170},
    JointDegreeRange{10, 160},
}

type JointDegreeRange struct {
    Min float64
    Max float64
}

type JointDegree struct {
    Degree float64
    Range  *JointDegreeRange
}

type JointDegrees []JointDegree

type LegPosition struct {
    X            float64
    Y            float64
    Z            float64
    JointDegrees JointDegrees
}

type LegPositions map[int]*LegPosition
"""

JointDegreeRange_lens = 2
JointDegree_lens = 3
JointDegrees_lens = 9  # 3 * JointDegree_lens
LegPosition_lens = 12    # 3 + 3*3  # 3 + JointDegrees_lens
LegPositions_lens = 72   # 6 * (3 + 3*3)


class HexaLeg():
    def __init__(self, conn):
        self.conn = conn
        self.func_execute = func_execute(self.conn, "HexaLeg")

    # The coordinate is the Leg-coordinate. The x range is -168mm-168mm, y range is 0mm-194mm,
    #  z range is -135mm-135mm.
    # joint degrees: d1, d2, d3
    def CalculateJointDegrees(self, x, y, z):
        param_list = [[DATA_FLOAT64, x],
                      [DATA_FLOAT64, y],
                      [DATA_FLOAT64, z]]
        ret = self.func_execute("MoveJoint", param_list)
        return ret

    # PitchRoll returns LegPositions transformed from given pitchAngle and rollAngle degrees.
    # return: 6*6 = 36 dims:
    # 6 * [X, Y, Z, d1, d2, d3]
    def PitchRoll(self, pitchAngle, rollAngle):  # return LegPositions
        ret = self.func_execute("PitchRoll", [[DATA_FLOAT64, pitchAngle],
                                            [DATA_FLOAT64, rollAngle]])
        return ret

    # MoveJoint rotates specified joint on a leg to a given degree in given duration.
    # The range of degree is different. The range of NO.0 joint's degree is (35 - 145).
    # The range of NO.1 joint's degree is (10 - 170). The range of NO.2 joint's degree is (10 - 160).
    def MoveJoint(self, legNumber, jointNumber, degree, duration):
        param_list = [[DATA_FLOAT64, legNumber],
                      [DATA_FLOAT64, jointNumber],
                      [DATA_FLOAT64, degree],
                      [DATA_FLOAT64, duration]]
        ret = 1 if self.func_execute("MoveJoint",
                                     param_list) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    """
    # MoveLeg moves a leg to specified position in given duration.
    # legNumber: 0~5
    # legPosition: [X, Y, Z, J1_d, J2_d, J3_d]: coordinate and degree of every joint
    def MoveLeg(self, legNumber, legPosition, duration):
        return

    # MoveLegs moves the legs in legPositions to specified positions in given duration.
    # move all
    def MoveLegs(self, legPositions, duration):
        return
    """

    # moves the legs to specified Coordinates in given duration.
    def MoveLeg_Coordinates(self, legNumber, x, y, z, duration):
        param_list = [[DATA_FLOAT64, legNumber],
                      [DATA_FLOAT64, x],
                      [DATA_FLOAT64, y],
                      [DATA_FLOAT64, z],
                      [DATA_FLOAT64, duration]]
        ret = 1 if self.func_execute("MoveLeg_Coordinates",
                                     param_list) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # moves the legs to specified JointDegrees in given duration.
    def MoveLeg_JointDegrees(self, legNumber, d1, d2, d3, duration):
        param_list = [[DATA_FLOAT64, legNumber],
                      [DATA_FLOAT64, d1],
                      [DATA_FLOAT64, d2],
                      [DATA_FLOAT64, d3],
                      [DATA_FLOAT64, duration]]
        ret = 1 if self.func_execute("MoveLeg_JointDegrees",
                                     param_list) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # moves the legs to specified Coordinates in given duration.
    def MoveLegs_Coordinates(self, legs, Coordinates, duration):
        leg_nums = len(legs)
        param_list = [[DATA_FLOAT64, leg_nums]]
        for i in range(len(legs)):
            param_list.append([DATA_FLOAT64, legs[i]])
        for i in range(len(Coordinates)):
            for j in range(len(Coordinates[i])):
                param_list.append([DATA_FLOAT64, Coordinates[i][j]])
        param_list.append([DATA_FLOAT64, duration])
        ret = 1 if self.func_execute("MoveLegs_Coordinates",
                                     param_list) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # moves the legs to specified JointDegrees in given duration.: len(legs) * 3 + 1
    def MoveLegs_JointDegrees(self, params):  # legs, JointDegrees, duration):
        # leg_nums: params[0]
        # JointDegrees: len(legs) * 3
        # duration
        param_list = [[DATA_FLOAT64, v] for v in params]
        """
        param_list = [[DATA_FLOAT64, leg_nums]]
        for i in range(len(legs)):
            param_list.append([DATA_FLOAT64, legs[i]])
        for i in range(len(JointDegrees)):
            for j in range(len(JointDegrees[i])):
                param_list.append([DATA_FLOAT64, JointDegrees[i][j]])
        param_list.append([DATA_FLOAT64, duration])
        """
        ret = 1 if self.func_execute("MoveLegs_JointDegrees",
                                     param_list) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # RelaxLegs reduces servo power in all the legs to save battery
    def RelaxLegs(self):
        ret = 1 if self.func_execute("RelaxLegs") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # stops movement of specified leg.
    def StopLeg(self, params):
        # legNumber = params[0]
        param_list = [[DATA_FLOAT64, v] for v in params]
        ret = 1 if self.func_execute("StopLeg", param_list) == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # StopLegs stops movement in all legs.
    def StopLegs(self):
        ret = 1 if self.func_execute("StopLegs") == SUCCESS_RESPONSE_FLAG else 0
        return ret

