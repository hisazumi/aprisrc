from time import sleep
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error

class Command:
    def __init__(self, type, parameter):
        self.type = type
        self.parameter = parameter

class Sequencer:
    def __init__(self, commands):
        self.tello = tellopy.Tello()
        self.commands = commands
        self.activity = {
            'takeoff': self.tello.takeoff,
            'land' : self.tello.land
        }

    def initialize(self):
        self.tello.connect()
        self.tello.wait_for_connection()
        # self.tello.video_encoder_rate = 1
        # self.tello.start_video()

    def run(self):
        self.tello.takeoff()
        sleep(5)
        self.tello.forward(50)
        sleep(5)
        self.tello.clockwise(180)
        sleep(5)
        self.tello.forward(50)
        sleep(5)
        self.tello.land()

ss = Sequencer([
    Command('takeoff', False),
    Command('sleep', 5),
    Command('land', False)
])
#ss.initialize()
#ss.run()
