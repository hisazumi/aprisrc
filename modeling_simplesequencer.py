from time import sleep, time
import threading
import traceback
import numpy as np
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import tellopy

class SimpleSequencer:
    def __init__(self):
        self.tello = False
        self.video_thread = False

    def video_receiver(self):
        dictionary_name = cv2.aruco.DICT_7X7_100
        dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)

        preids_list = []
        preids = set([])    # set variable
        preids = set(preids_list)

        try:
            container = av.open(self.tello.get_video_stream())
            # skip first 300 frames
            frame_skip = 300
            while True:
                for frame in container.decode(video=0):
                    if 0 < frame_skip:
                        frame_skip = frame_skip - 1
                        continue

                    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(np.array(frame.to_image()), dictionary)
                    start_time = time()	# elapsed time(second) from 1970/1/1 00:00;00
                    image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                    image = cv2.aruco.drawDetectedMarkers(np.array(image), corners, ids)

                    if isinstance(ids, np.ndarray) == True:
                        for elem in ids:
                            preids_list = list(elem)
                            value = preids_list[0]
                            preids.add(value)
                        print('Detected ArMark ID=', preids)

                    # Get height and width of read image
                    height = int(image.shape[0]/2)
                    width = int(image.shape[1]/2)
                    resized_img = cv2.resize(image,(width,height))
                    cv2.imshow('Original', resized_img)
                    cv2.waitKey(1)
                    frame_skip = int((time() - start_time)/frame.time_base) * 50

        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print(ex)
        finally:
            cv2.destroyAllWindows()

    def initialize(self):
        self.tello = tellopy.Tello()
        self.tello.connect()
        self.tello.wait_for_connection()
        self.tello.video_encoder_rate = 1
        self.tello.start_video()
        self.video_thread = threading.Thread(target=self.video_receiver)
        self.video_thread.start()

    def run(self):
        sleep(10)
        self.tello.takeoff()
        sleep(5)
        self.tello.forward(10)
        sleep(5)
        self.tello.clockwise(180)
        sleep(5)
        self.tello.forward(10)
        sleep(5)
        self.tello.land()

    def stop(self):
        self.tello.quit()


ss = False
try:
    ss = SimpleSequencer()
    ss.initialize()
    #ss.run()
    sleep(100)
except KeyboardInterrupt as e:
    print(e)
except Exception as e:
    print(e)

ss.stop()

