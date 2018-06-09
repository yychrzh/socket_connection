#-*-coding:utf-8-*-
from remote_robot import func_execute

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


# Package accelerometer provides an API for interfacing with the HEXA's accelerometer.
# Example: Get current acceleration and degree of inclination.
# accelerometer.Start()
# fx, fy, fz, ax, ay, az, err := accelerometer.Value()
# accelerometer.Close()
class Accelerometer():
    def __init__(self, conn):
        self.conn = conn
        self.func_execute = func_execute(self.conn, "Acce")

    # Available returns whether driver is available or not.
    def Available(self):  # return data: bool
        ret = self.func_execute("Available")[0]
        return ret

    # Start starts the accelerometer driver.
    def Start(self):      # return data: error info
        ret = 1 if self.func_execute("Start") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Close shuts down the accelerometer driver.
    def Close(self):
        ret = 1 if self.func_execute("Close") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Value returns the current acceleration exhibited on the HEXA as well as
    # its inclination (a). When HEXA is standing still fz will be equal to ~9.8.
    # Any movement on the HEXA will affect the values returned meaning accurate
    # angles can only be mesaured when the HEXA is standing still.
    # fx, fy, fz are current acceleration and ax, ay, az are angles in degrees.
    def Value(self):
        ret = self.func_execute("Value")
        return ret


# Package distance provides API for the distance sensor.
# Example: Getting the current distance.
# distance.Start()
# dist := distance.Value()
# distance.Close()
class Distance():
    def __init__(self, conn):
        self.conn = conn
        self.func_execute = func_execute(self.conn, "Distance")

    # Available returns whether driver is available or not.
    def Available(self):  # return data: bool
        ret = self.func_execute("Available")[0]
        return ret

    # Start starts the distance sensor driver.
    def Start(self):      # return data: error info
        ret = 1 if self.func_execute("Start") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Close shuts down the distance sensor driver.
    def Close(self):
        ret = 1 if self.func_execute("Close") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Value returns the filtered distance value within the range of 100~1500mm
    def Value(self):
        ret = self.func_execute("Value")[0]
        return ret


# Package infrared provides an API to interface with the infrared module.
class Infrared():
    def __init__(self, conn):
        self.conn = conn
        self.func_execute = func_execute(self.conn, "Infrared")

    # Available returns whether driver is available or not.
    def Available(self):  # return data: bool
        ret = self.func_execute("Available")[0]
        return ret

    # Start makes sure the infrared module driver is ready.
    def Start(self):      # return data: error info
        ret = 1 if self.func_execute("Start") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Close makes sure the infrared module driver is shut down.
    def Close(self):
        ret = 1 if self.func_execute("Close") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # Value returns the filtered distance value within the range of 100~1500mm
    def Value(self):
        ret = self.func_execute("Value")[0]
        return ret

    # LightOn starts the emitting of infrared light without modulated information.
    def LightOn(self):
        ret = 1 if self.func_execute("LightOn") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    def LightOff(self):
        ret = 1 if self.func_execute("LightOff") == SUCCESS_RESPONSE_FLAG else 0
        return ret

    # SendInfraredSequence takes a slice of pulses and gaps in duration
    # (microseconds) and sends them to the infrared device. The length of the
    # slice has to be an odd number and start with, as well as end with a
    # pulse duration.
    # Example: Send a sequence to the infrared device.
    # infrared.Start()
    # sequence := []int{2416, 582, 1204, 585, 609, 580, 1752, 33, 608, 577, 1574}
    # infrared.SendInfraredSequence(sequence)
    # infrared.Close()
    def SendInfraredSequence(self, sequence):
        param_list = [[DATA_FLOAT64, sequence[i]] for i in range(len(sequence))]
        ret = 1 if self.func_execute("SendInfraredSequence",
                                     param_list) == SUCCESS_RESPONSE_FLAG else 0
        return ret

