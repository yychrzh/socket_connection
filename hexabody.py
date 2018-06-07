#-*-coding:utf-8-*-
# for vincross hexa robot:


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
JointDegreeRange = [[35, 145], [10, 170], [10, 160]]


class hexa_head(object):
    def __init__(self, state):
        self.direction = self.Direction()
        self.duration = 0
        self.state = state  # relax or not

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
        degree = degree if degree > JointDegreeRange[num][0] else JointDegreeRange[num][0]
        degree = degree if degree < JointDegreeRange[num][1] else JointDegreeRange[num][1]
        duration = duration if duration > Min_duration else Min_duration
        duration = duration if duration < Max_duration else Max_duration
        self.joint_degree[num] = degree
        self.duration[num] = duration

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
    def Lift(self):
        return 0

    # Pitch makes the body pitch at specified degree of angle in given duration.
    # The HEXA will pitch along the X axis of body coordinate.
    def Pitch(self):
        return 0

    # StopPitching stops an ongoing pitch.
    def StopPitch(self):
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
        return 0


class hexabody(object):
    def __init__(self):
        pass

    # Available returns whether driver is available or not.
    def Available(self):
        return 0

    # Start starts the hexabody driver.
    def Start(self):
        return 0

    # Releax reduces power to all servos on HEXA to save battery.
    def Relax(self):
        return 0

    # Close shuts down the hexabody driver.
    def Close(self):
        return 0


if __name__ == "__main__":
    pass
