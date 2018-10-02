"""
tellopy sample using joystick and video palyer

 - you can use PS3/PS4/XONE joystick to controll DJI Tello with tellopy module
 - you must install mplayer to replay the video
 - Xbox One Controllers were only tested on Mac OS with the 360Controller Driver.
    get it here -> https://github.com/360Controller/360Controller'''
"""

import time
import sys
import tellopy
import traceback
import cv2.cv2 as cv2  # for avoidance of pylint error
import av
import numpy
from pynput.keyboard import Key, Listener


prev_flight_data = None

def flight_data_handler(event, sender, data, **args):
    global prev_flight_data
    if prev_flight_data != str(data):
        print(data)
        prev_flight_data = str(data)


skip_frames = 300
drone = None
container = None
dictionary_name = cv2.aruco.DICT_4X4_50 
dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)

def on_press(key):
    key_code = format(key.char)
    print('{0} pressed'.format(key_code))
    if key_code == 't':
        print("Start Take-Off!")
        drone.takeoff()
        time.sleep(5)
    elif key_code == 'l':
        print("Start Landing!")
        drone.down(50)
        time.sleep(5)
        drone.land()
    elif key_code == "Key.left":
        print("left")
        drone.left(20)
    elif key_code == "Key.right":
        print("right")
        drone.right(20)
    elif key_code == "Key.up":
        print("forward")
        drone.forward(20)
        time.sleep(1)
    elif key_code == "Key.down":
        drone.backward(20)

def on_release(key):
    key_code = format(key.char)
    print('{0} released'.format(key_code))
    drone.forward(0)
    drone.backward(0)
    drone.right(0)
    drone.left(0)

def video_handler():
    global container
    global skip_frames

    try:
        for frame in container.decode(video=0):
            if 0 < skip_frames:
                skip_frames -= 1
            else:
                corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(numpy.array(frame.to_image()), dictionary)
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                image = cv2.aruco.drawDetectedMarkers(numpy.array(image), corners, ids)
                # 読み込んだ画像の高さと幅を取得
                height = int(image.shape[0]/2)
                width = int(image.shape[1]/2)
                resized_img = cv2.resize(image,(width,height))
                cv2.imshow('Original', resized_img)
                cv2.waitKey(1)
                skip_frames = int((time.time() - start_time)/frame.time_base)
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

def main():
    global container, drone

    drone = tellopy.Tello()
    drone.video_encoder_rate = 1
    drone.connect()
    drone.wait_for_connection(60.0)
    container = av.open(drone.get_video_stream())
    drone.subscribe(drone.EVENT_FLIGHT_DATA, flight_data_handler)

    listener = Listener(on_press = on_press, on_release= on_release)
    listener.start()

    try:
        while True:
            # loop with pygame.event.get() is too much tight w/o some sleep
            video_handler()
            time.sleep(0.01)

    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)

    cv2.destroyAllWindows()
    drone.quit()
    exit(1)


if __name__ == '__main__':
    main()
