#-*-coding:utf-8-*-

# Package hexabody provides an API to interface with the HEXAS's body.
# HEXA has six legs and each leg has three joints, including the head joint the DOF(degree of freedom) is 19.
# When animating a movement, duration (ms) will be passed as an argument when the distance to the new location is
# known, otherwise speed (cm/s for movements and degree/s for rotations) will passed. The range of duration is
# 0 ~ 9999ms. The duration longer than 9999ms will be set as 9999ms.
# All joint and leg positions are points in a Cartesian coordinate system.

# control instruction: (double)
#


# hexabody
Available = True
Start     = True
Relax     = False
Min_duration  = 0
Slow_duration = 30
Fast_duration = 500
Max_duration  = 9999

# head
MinDirection = 0
MaxDirection = 359

# legs
LegNumber = [0, 1, 2, 3, 4, 5]
JointNumber = [0, 1, 2]
LegLength = [59, 47, 88]
JointDegreeRanges = [[35, 145], [10, 170], [10, 160]]

# GaitType
GaitOriginal = 0   # default gait
GaitWave     = 1   # 5+1 gait, 5 legs stay on the ground and 1 leg raise at the same time
GaitRipple   = 2   # 4+2 gait, 4 legs stay on the ground and 2 legs raise at the same time
GaitTripod   = 3   # 3+3 gait, 3 legs stay on the ground and 3 legs raise at the same time
GaitAmble    = 4   # 4+2 gait, 4 legs stay on the ground and 2 legs raise at the same time, different from GaitRipple.


# JointDegreeRange defines the range of joint rotation.
class JointDegreeRange():
    def __init__(self):
        self.Min = 0
        self.MAx = 0


# JointDegree defines the degree and range of rotation of a joint.
class JointDegree():
    def __init__(self):
        self.Degree = 0
        self.JointDegreeRange = JointDegreeRange()

    # Fit ensures the joint in range, if it is out of range, it will be modified to the adjacent edge value.
    def Fit(self):
        return 0

    # IsValid returns whether joint degree is in range.
    def IsValid(self):
        return 0


# JointDegrees is a slice of JointDegree
class JointDegrees():
    def __init__(self):
        self.js = []

    # NewJointDegrees creates a new JointDegrees.
    def NewJointDegrees(self, j_num):
        self.Js = [JointDegree() for _ in range(j_num)]
        return 0

    # Fit ensures the joints in range, if any of them is out of range, it will be modified to the adjacent edge value.
    def Fit(self):
        return 0

    # IsValid returns whether joints degrees are in range.
    def IsValid(self):
        return 0

    # SetJointDegree sets the degree of the particular joint.
    def SetDegree(self, jointNumber, degree):
        return 0

    # SetJointDegrees sets the degrees of three joints.
    def SetDegrees(self, degree0, degree1, degree2):
        return 0


# LegPosition holds the points of a leg in the Cartesian coordinate system as well as
# the degree of rotation of the joints in the leg.
class LegPosition():
    def __init__(self):
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.JointDegrees = JointDegrees()

    # NewLegPosition returns new LegPosition with given (x, y, z). The coordinate is the Leg-coordinate.
    # The x range is -168mm-168mm, y range is 0mm-194mm, z range is -135mm-135mm.
    def NewLegPosition(self):
        return 0

    # CalculateJointDegrees calculates joints degree in single leg. It will convert the coordinate data of the leg
    # to joints' degree. 'JointNumberNotSupport' error will be returned if the count of joint are not 3.
    # 'OverflowHardLimit' error will be returned if the coordinate represent an unreachable place.
    def CalculateJointDegrees(self):
        return 0

    # Coordinates returns the legPosition's coordinates.
    # 'LegPositionInvalid' error will be returned if legPosition's coordinate is not valid.
    def Coordinates(self):
        return 0, 0, 0

    # Fit is used to approximate a reachable leg position for the LegPosition object.
    # 'JointNumberNotSupport' error will be returned if the count of joint are not 3.
    # 'OverflowHardLimit' error will be returned if the coordinate represent an unreachable place.
    def Fit(self):
        return 0

    # IsValid returns if the leg positions can be reached.
    def IsValid(self):
        return 0

    # SetCoordinates sets the position coordinates of a LegPosition.
    def SetCoordinates(self, x, y, z):  # return LegPosition
        return 0

    # SetJointDegrees sets the jointdegrees of a LegPosition.
    def SetJointDegrees(self, jointDegrees): # return LegPosition
        return 0


class LegPositions():
    def __init__(self):
        self.Lp = []

    # NewLegPositions creates a set of legPositions, then use SetLegPosition to put legPostion into it.
    def NewLegPositions(self, l_num):
        self.Lp = [LegPosition() for _ in range(l_num)]
        return 0

    # Fit is used to approximate reachable leg positions for every leg position in the LegPositions object.
    def Fit(self):
        return 0

    # IsValid returns if all of the leg positions can be reached.
    def IsValid(self):
        return 0

    # SetLegPosition set legPosition with legNumber.
    def SetLegPosition(self, legNumber, legPostion):
        return 0


class hexa_head(object):
    def __init__(self):
        self.direction = self.Direction()
        self.duration = 0

    # Direction returns the current direction of HEXA's head in degrees (0-359).
    # 0 degrees is in the direction of the power button. The result is the degree
    # between the head and the power button in an anti-clockwise rotation.
    def Direction(self):
        return 0

    # MoveHead moves the head to specified degree(0-359) in given duration.
    # 0 degrees is in the direction of the power button. An increase in direction
    # angle results in an anti-clockwise rotation.
    def MoveHead(self, degree, duration):
        self.direction = degree
        self.duration = duration

    # RelaxHead reduces servo energy to head to save battery.
    def RelaxHead(self):
        return 0

    # RotateHeadContinuously makes the head rotate continuously with specified direction and speed (1 - 360).
    def RotateHeadContinuously(self, direction, speed):
        return 0

    # RotatingHeadContinuously returns whether HEXA is rotating it's head continuously or not.
    def RotatingHeadContinuously(self):
        return 0

    # StopRotatingHeadContinuously stops continuous rotation of the head.
    def StopRotatingHeadContinuously(self):
        return 0


# one leg of hexa robot
class hexa_leg(object):
    def __init__(self, legNum):
        self.legNum = legNum
        self.joint_degree = [0, 0, 0]
        self.duration = [0, 0, 0]

    # MoveJoint rotates specified joint on a leg to a given degree in given duration.
    # The range of degree is different. The range of NO.0 joint's degree is (35 - 145).
    # The range of NO.1 joint's degree is (10 - 170). The range of NO.2 joint's degree is (10 - 160).
    def MoveJoint(self, num, degree, duration):
        return 0

    # MoveLeg moves a leg to specified position in given duration.
    def MoveLeg(self, joint_degree, duration):
        for n in JointNumber:
            self.MoveJoint(n, joint_degree[n], duration)

    # stops movement of specified leg.
    def StopLeg(self):
        return 0


class hexa_legs(object):
    def __init__(self):
        self.legs = []
        for n in LegNumber:
            self.legs.append(hexa_leg(n))

    # num: 0~2
    def MoveJoint(self, leg_num, joint_num, degree, duration):
        self.legs[leg_num].MoveJoint(joint_num, degree, duration)

    def MoveLeg(self, leg_num, joint_degree, duration):
        self.legs[leg_num].MoveLeg(joint_degree, duration)

    # RelaxLegs reduces servo power in all the legs to save battery.
    def RelaxLegs(self):
        return 0

    # StopLegs stops movement in all legs.
    def StopLegs(self):
        return 0


class hexa_body(object):
    def __init__(self):
        pass

    # Lift raises or reduces the height of HEXA's body in given height (-20 mm - 50 mm).
    def Lift(self, height):
        return 0

    # Pitch makes the body pitch at specified degree of angle in given duration.
    # The HEXA will pitch along the X axis of body coordinate.
    def Pitch(self, degree, duration):
        return 0

    # StopPitching stops an ongoing pitch.
    def StopPitch(self):
        return 0

    # PitchRoll returns LegPositions transformed from given pitchAngle and rollAngle degrees.
    def PitchRoll(self, pitchAngle, rollAngle):  # return LegPositions
        return 0

    # Stand makes the HEXA stand at the default height of 50mm.
    def Stand(self):
        return 0

    # StandWithHeight makes the HEXA stand with it's body at the specified height
    def StandWithHeight(self, height):
        return 0

    # SelectGait chooses the walking gait of HEXA. 'SelectGaitWhileWalking' error will be returned
    # if the HEXA is walking. 'WrongGaitType' error will be returned if a wrong gait type is input.
    def SelectGait(self, gaitType):
        return 0

    # SetStepLength set the walking step length of HEXA. The range of stepLengthRatio is (0, 1].
    # 'OverflowStepLengthRatio' error will be returned if stepLengthRatio is out of its range.
    def SetStepLength(self, stepLengthRatio):
        return 0

    # Spin makes the HEXA use its legs to position itself in the given degree of rotation in given duration.
    def Spin(self, degree, duration):
        return 0

    # Marching is a kind of state of the walk. The leg of HEXA will be raised higher when it's walking.
    # It's different from the gait of the walk. StartMarching makes the HEXA enter the state of marching.
    def StartMarching(self):
        return 0

    # StopMarching makes the HEXA quit the state of marching.
    def StopMarching(self):
        return

    # WalkContinuously makes the HEXA walk continuously in given direction in degrees (0-359)
    # with given speed (0.1 cm/s - 1.2 cm/s). Call StopWalkingContinuously to stop.
    # 0 degrees is in the direction of the power button.
    # An increase in direction angle results in an anti-clockwise rotation.
    def WalkContinuously(self, direction, speed):
        return

    # WalkingContinuously returns whether HEXA is walking continuously or not.
    def WalkingContinuously(self):
        return

    # StopWalkingContinuously stops the HEXA from walking continuously.
    def StopWalkingContinuously(self):
        return

    # Walk makes the HEXA walk one frame in given direction in degrees (0-359) with given duration.
    # Calling this function in a loop would give the same effect as calling WalkContinuously.
    # 0 degrees is in the direction of the power button. An increase in direction angle results in
    # an anti-clockwise rotation.
    def Walk(self, direction, duration):
        return


# hexa's top instructions
class hexa(object):
    def __init__(self):
        pass

    # Available returns whether driver is available or not.
    def Available(self):
        return

    # Start starts the hexabody driver.
    def Start(self):
        return

    # Releax reduces power to all servos on HEXA to save battery.
    def Relax(self):
        return

    # Close shuts down the hexabody driver.
    def Close(self):
        return


if __name__ == "__main__":
    pass
