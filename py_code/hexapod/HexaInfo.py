# GaitType
GaitOriginal = 0   # default gait
GaitWave     = 1   # 5+1 gait, 5 legs stay on the ground and 1 leg raise at the same time
GaitRipple   = 2   # 4+2 gait, 4 legs stay on the ground and 2 legs raise at the same time
GaitTripod   = 3   # 3+3 gait, 3 legs stay on the ground and 3 legs raise at the same time
GaitAmble    = 4   # 4+2 gait, 4 legs stay on the ground and 2 legs raise at the same time, different from GaitRipple.


module_list = ["Hexa", "HexaBody", "HexaHead", "HexaLeg", "Acce", "Distance", "Infrared", "SensorWalk", "AutoRun"]


function_list = {
    "Hexa": ["Available", "Start", "Relax", "Close", "RobotInfo"],
    "HexaBody": ["Lift", "Pitch", "StopPitch", "Stand", "StandWithHeight", "SelectGait",
                 "SetStepLength", "Spin", "StartMarching", "StopMarching", "WalkContinuously",
                 "WalkingContinuously", "StopWalkingContinuously", "Walk"],
    "HexaHead": ["Direction", "MoveHead", "RelaxHead", "RotateHeadContinuously",
                 "RotatingHeadContinuously", "StopRotatingHeadContinuously"],
    "HexaLeg": ["CalculateJointDegrees", "PitchRoll", "MoveJoint", "MoveLeg_Coordinates",
                "MoveLeg_JointDegrees", "MoveLegs_Coordinates", "MoveLegs_JointDegrees",
                "RelaxLegs", "StopLeg", "StopLegs"],
    "Acce": ["Available", "Start", "Close", "Value"],
    "Distance": ["Available", "Start", "Close", "Value"],
    "Infrared": ["Available", "Start", "Close", "LightOn", "LightOff", "SendInfraredSequence"]
    "SensorWalk": ["Init", "Start", "Stop", "Close"],
    "AutoRun": ["Init", "Start", "Stop", "Close"]
}


# param_list:
# module_name=>function_name=>[input params name list, return nums]
function_in_out_list = {
    "Hexa": {"Available": [0, ["state"]], "Start": [0, 0], "Relax": [0, 0], "Close": [0, 0],
             "RobotInfo": [0, ["Battery", "Temperature", "IsCharging"]]},

    "HexaBody": {
                 "Lift": [["height"], 0],
                 "Pitch": [["degree", "duration"], 0],
                 "StopPitch": [0, 0],
                 "Stand": [0, 0],
                 "StandWithHeight": [["height"], 0],
                 "SelectGait": [["gaitType"], 0],
                 "SetStepLength": [["stepLengthRatio"], 0],
                 "Spin": [["degree", "duration"], 0],
                 "StartMarching": [0, 0],
                 "StopMarching": [0, 0],
                 "WalkContinuously": [["direction", "speed"], 0],
                 "WalkingContinuously": [0, ["state"]],
                 "StopWalkingContinuously": [0, 0],
                 "Walk": [["direction", "duration"], 0]},

    "HexaHead": {
                 "Direction": [0, ["head_direction"]],
                 "MoveHead": [["direction", "duration"], 0],
                 "RelaxHead": [0, 0],
                 "RotateHeadContinuously": [["direction", "speed"], 0],
                 "RotatingHeadContinuously": [0, ["state"]],
                 "StopRotatingHeadContinuously": [0, 0]},

    "HexaLeg": {
                "CalculateJointDegrees": [["Coordinate_X", "Coordinate_Y", "Coordinate_Z"],
                                          ["leg0_JointDegrees(d0, d1, d2)",
                                           "leg1_JointDegrees(d0, d1, d1)",
                                           "leg2_JointDegrees(d0, d1, d2)",
                                           "leg3_JointDegrees(d0, d1, d2)",
                                           "leg4_JointDegrees(d0, d1, d2)",
                                           "leg5_JointDegrees(d0, d1, d2)"]],
                "PitchRoll": [["pitchAngle", "rollAngle"],
                              ["leg0_position(X, Y, Z, d0, d1, d2)",
                               "leg1_position(X, Y, Z, d0, d1, d2)",
                               "leg2_position(X, Y, Z, d0, d1, d2)",
                               "leg3_position(X, Y, Z, d0, d1, d2)",
                               "leg4_position(X, Y, Z, d0, d1, d2)",
                               "leg5_position(X, Y, Z, d0, d1, d2)"]],
                "MoveJoint": [["legNumber", "jointNumber", "degree", "duration"], 0],
                "MoveLeg_Coordinates": [["legNumber", "Coordinate_X", "Coordinate_Y",
                                         "Coordinate_Z", "duration"], 0],
                "MoveLeg_JointDegrees": [["legNumber", "degree0", "degree1", "degree2",
                                          "duration"], 0],
                "MoveLegs_Coordinates": [["leg_nums", "leg_num_list(leg_nums:0~5)",
                                          "Coordinates(leg_nums * 3)", "duration"], 0],
                "MoveLegs_JointDegrees": [["leg_nums", "leg_num_list(leg_nums:0~5)",
                                           "JointDegrees(leg_nums * 3)", "duration"], 0],
                "RelaxLegs": [0, 0],
                "StopLeg": [["legNumber"], 0],
                "StopLegs": [0, 0]},

    "Acce": {"Available": [0, ["state"]], "Start": [0, 0], "Close": [0, 0],
             "Value": [0, ["fx", "fy", "fz", "ax", "ay", "az"]]},

    "Distance": {"Available": [0, ["state"]], "Start": [0, 0], "Close": [0, 0],
                 "Value": [0, ["distance"]]},

    "Infrared": {"Available": [0, ["state"]], "Start": [0, 0], "Close": [0, 0],
                 "LightOn": [0, 0], "LightOff": [0, 0],
                 "SendInfraredSequence": [["sequence"], 0]},
    "SensorWalk": {"Init": [0, 0], "Start": [["walk_speed", "gaitType"], 0], "Stop": [0, 0], "Close": [0, 0]},
    "AutoRun": {"Init": [0, 0], "Start": [["walk_speed", "gaitType"], 0], "Stop": [0, 0], "Close": [0, 0]}
}


# param_list:
# module_name=>function_name=>[input params name list, return nums]
function_description_list = {
    "Hexa": {"Available": "Available returns whether driver is available or not.",
             "Start": "Start starts the hexabody driver.",
             "Relax": "Releax reduces power to all servos on HEXA to save battery.",
             "Close": "Close shuts down the hexabody driver.",
             "RobotInfo": "Robotinfo calls the robot to return the infomation of " +
                          "Battery(0~1), Temperature(centigrade) and IsCharging"},

    "HexaBody": {
                 "Lift": "Lift raises or reduces the height of HEXA's body in given " +
                         "height (-20 mm - 50 mm).",
                 "Pitch": "Pitch makes the body pitch at specified degree of angle " +
                          "in given duration. The HEXA will pitch along the X axis " +
                          "of body coordinate.",
                 "StopPitch": "StopPitching stops an ongoing pitch.",
                 "Stand": "Stand makes the HEXA stand at the default height of 50mm.",
                 "StandWithHeight": "StandWithHeight makes the HEXA stand with it's " +
                                    "body at the specified height",
                 "SelectGait": "SelectGait chooses the walking gait of HEXA. 'SelectGa" +
                               "itWhileWalking' error will be returned if the HEXA is " +
                               "walking. 'WrongGaitType' error will be returned if a " +
                               "wrong gait type is input.",
                 "SetStepLength": "SetStepLength set the walking step length of HEXA. " +
                                  "The range of stepLengthRatio is (0, 1]. 'OverflowSte" +
                                  "pLengthRatio' error will be returned if stepLengthRatio " +
                                  "is out of its range.",
                 "Spin": "Spin makes the HEXA use its legs to position itself in the given " +
                         "degree of rotation in given duration.",
                 "StartMarching": "Marching is a kind of state of the walk. The leg of HEXA" +
                                  " will be raised higher when it's walking. It's different " +
                                  "from the gait of the walk. StartMarching makes the HEXA" +
                                  " enter the state of marching.",
                 "StopMarching": "StopMarching makes the HEXA quit the state of marching.",
                 "WalkContinuously": "WalkContinuously makes the HEXA walk continuously in" +
                                     " given direction in degrees (0-359) with given speed " +
                                     "(0.1 cm/s - 1.2 cm/s). Call StopWalkingContinuously " +
                                     "to stop. 0 degrees is in the direction of the power button." +
                                     "An increase in direction angle results in an anti-clockwise " +
                                     "rotation.",
                 "WalkingContinuously": "WalkingContinuously returns whether HEXA is walking " +
                                        "continuously or not.",
                 "StopWalkingContinuously": "StopWalkingContinuously stops the HEXA from walking " +
                                            "continuously.",
                 "Walk": "Walk makes the HEXA walk one frame in given direction in degrees (0-359) " +
                         "with given duration. Calling this function in a loop would give the same " +
                         "effect as calling WalkContinuously. 0 degrees is in the direction of the " +
                         "power button. An increase in direction angle results in an anti-clockwise " +
                         "rotation."},

    "HexaHead": {
                 "Direction": "Direction returns the current direction of HEXA's head in degrees " +
                              "(0-359). 0 degrees is in the direction of the power button. The " +
                              "result is the degree between the head and the power button in an " +
                              "anti-clockwise rotation.",
                 "MoveHead": "MoveHead moves the head to specified degree(0-359) in given duration." +
                             "0 degrees is in the direction of the power button. An increase in" +
                             " direction angle results in an anti-clockwise rotation.",
                 "RelaxHead": "RelaxHead reduces servo energy to head to save battery.",
                 "RotateHeadContinuously": "RotateHeadContinuously makes the head rotate continuously" +
                                           " with specified direction and speed (1 - 360).",
                 "RotatingHeadContinuously": "RotatingHeadContinuously returns whether HEXA is rotating" +
                                             " it's head continuously or not.",
                 "StopRotatingHeadContinuously": "StopRotatingHeadContinuously stops continuous " +
                                                 "rotation of the head."},

    "HexaLeg": {
                "CalculateJointDegrees": "The coordinate is the Leg-coordinate. The x range is " +
                                         "-168mm-168mm, y range is 0mm-194mm, z range is " +
                                         "-135mm-135mm. joint degrees: d0, d1, d2",
                "PitchRoll": "PitchRoll returns LegPositions transformed from given pitchAngle " +
                             "and rollAngle degrees. return: 6*6 = 36 dims: 6 * [X, Y, Z, d1, d2, d3]",
                "MoveJoint": "MoveJoint rotates specified joint on a leg to a given degree in given " +
                             "duration. The range of degree is different. The range of NO.0 joint's " +
                             "degree is (35 - 145). The range of NO.1 joint's degree is (10 - 170). " +
                             "The range of NO.2 joint's degree is (10 - 160).",
                "MoveLeg_Coordinates": "moves the legs to specified Coordinates in given duration.",
                "MoveLeg_JointDegrees": "moves the legs to specified JointDegrees in given duration.",
                "MoveLegs_Coordinates": "moves the legs to specified Coordinates in given duration.",
                "MoveLegs_JointDegrees": "moves the legs to specified JointDegrees in given duration.: " +
                                         "len(legs) * 3 + 1",
                "RelaxLegs": "RelaxLegs reduces servo power in all the legs to save battery.",
                "StopLeg": "stops movement of specified leg.",
                "StopLegs": "StopLegs stops movement in all legs."},

    "Acce": {"Available": "Available returns whether driver is available or not.",
             "Start": "Start starts the accelerometer driver.",
             "Close": "Close shuts down the accelerometer driver.",
             "Value": "Value returns the current acceleration exhibited on the HEXA as well as " +
                      "its inclination (a). When HEXA is standing still fz will be equal to ~9.8." +
                      "Any movement on the HEXA will affect the values returned meaning accurate" +
                      "angles can only be mesaured when the HEXA is standing still." +
                      "fx, fy, fz are current acceleration and ax, ay, az are angles in degrees."},

    "Distance": {"Available": "Available returns whether driver is available or not.",
                 "Start": "Start starts the distance sensor driver.",
                 "Close": "Close shuts down the distance sensor driver.",
                 "Value": "Value returns the filtered distance value within the range of 100~1500mm."},

    "Infrared": {"Available": "Available returns whether driver is available or not.",
                 "Start": "Start makes sure the infrared module driver is ready.",
                 "Close": "Close makes sure the infrared module driver is shut down.",
                 "LightOn": "LightOn starts the emitting of infrared light without modulated information.",
                 "LightOff": "LightOff turns off the light.",
                 "SendInfraredSequence": "SendInfraredSequence takes a slice of pulses and gaps in duration" +
                 "(microseconds) and sends them to the infrared device. The length of the" +
                 "slice has to be an odd number and start with, as well as end with a pulse duration." +
                 "\nExample: Send a sequence to the infrared device.\ninfrared.Start()\nsequence := " +
                 "[]int{2416, 582, 1204, 585, 609, 580, 1752, 33, 608, 577, 1574}\ninfrared."
                 "SendInfraredSequence(sequence)\ninfrared.Close()"}
    "SensorWalk": {"Init": [0, 0], "Start": [["walk_speed", "gaitType"], 0], "Stop": [0, 0], "Close": [0, 0]},
    "AutoRun": {"Init": [0, 0], "Start": [["walk_speed", "gaitType"], 0], "Stop": [0, 0], "Close": [0, 0]}
}



