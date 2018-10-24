from time import sleep
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error

class SimpleSequencer:
    def __init__(self):
        self.tello = False

    def initialize(self):
        self.tello = tellopy.Tello()
        self.tello.connect()
        self.tello.wait_for_connection()
        # self.tello.video_encoder_rate = 1
        # self.tello.start_video()

    def run(self):
        try:
            self.tello.takeoff()
            sleep(5)
            self.tello.forward(50)
            sleep(5)
            self.tello.clockwise(180)
            sleep(5)
            self.tello.forward(50)
            sleep(5)
            self.tello.land()
        except KeyboardInterrupt as e:
            print(e)
        except Exception as e:
            print(e)

        drone.quit()
        exit(1)


ss = SimpleSequencer()
ss.initialize()
ss.run()
