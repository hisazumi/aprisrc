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
from subprocess import Popen, PIPE

import traceback
#import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time

from pynput.keyboard import Key, Listener

prev_flight_data = None
video_player = None


def handler(event, sender, data, **args):
    global prev_flight_data
    global video_player
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        if prev_flight_data != str(data):
            print(data)
            prev_flight_data = str(data)
    elif event is drone.EVENT_VIDEO_FRAME:
        if video_player is None:
            video_player = Popen(['mplayer', '-fps', '35', '-'], stdin=PIPE)
        try:
            video_player.stdin.write(data)
        except IOError as err:
            print(err)
            video_player = None
    else:
        print('event="%s" data=%s' % (event.getname(), str(data)))


def update(old, new, max_delta=0.3):
    if abs(old - new) <= max_delta:
        res = new
    else:
        res = 0.0
    return res



key_code=0
key_condition=0
key_timing = 0


def on_press(key):
    global key_code, key_condition, key_timing
    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        key_code = format(key.char)
    except AttributeError:
        #print('special key {0} pressed'.format(key))
        key_code = format(key)
    key_condition = 1
    key_timing = 1


def on_release(key):
    global key_code, key_condition, key_timing
    #print('{0} released'.format(key))
    key_condition = 0
    key_code = format(key)
    key_timing = 1

from time import sleep
import tellopy


def main():

    global key_code, key_condition,key_timing
    condition = 0;
    direct = 0

    drone = tellopy.Tello()
    drone.video_encoder_rate = 1
    drone.connect()
    drone.start_video()
    drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
    drone.subscribe(drone.EVENT_VIDEO_FRAME, handler)
    speed = 100
    throttle = 0.0
    yaw = 0.0
    pitch = 0.0
    roll = 0.0

    listener = Listener(on_press = on_press,on_release= on_release)
    listener.start()


    try:
        while 1:
            # loop with pygame.event.get() is too much tight w/o some sleep
            time.sleep(0.01)

            if key_timing  == 1: # key change 
                key_timing = 0;
                if key_condition == 1: #key_condition = 1 press
                    print('alphanumeric key {0} pressed'.format(key_code))
                    if key_code == 't'and condition == 0:
                        print("Start Take-Off!")
                        drone.takeoff()
                        sleep(5)
                        condition = 1
                    elif key_code == 'l'and condition == 1:
                        print("Start Landing!")
                        drone.down(50)
                        sleep(5)
                        drone.land()
                        condition = 0
                    elif key_code == "Key.left":
                        print("left")
                        drone.left(20)
                        direct=4
                    elif key_code == "Key.right":
                        print("right")
                        drone.right(20)
                        direct=3
                    elif key_code == "Key.up":
                        print("forward")
                        drone.forward(20)
                        sleep(1)
                        direct=1
                    elif key_code == "Key.down":
                        drone.backward(20)
                        direct=2
                    elif key_code == "Key.esc":
                        if condition == 1:
                            print("Start Landing!")
                            drone.down(50)
                            sleep(5)
                            drone.land()
                            condition = 0
                        break
                else: #key_condition=0 release
                    print('{0} released'.format(key_code))
                    if direct == 1:
                        drone.forward(0)
                    elif direct == 2:
                        drone.backward(0)
                    elif direct == 3:
                        drone.right(0)
                    elif direct == 4:
                        drone.left(0)
                    direct=0

    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)

    drone.quit()
    exit(1)


if __name__ == '__main__':
    main()
