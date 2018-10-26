import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time

dictionary_name = cv2.aruco.DICT_4X4_50 
dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)

def main():
    drone = tellopy.Tello()
    drone.video_encoder_rate = 1

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        container = av.open(drone.get_video_stream())
        # skip first 300 frames
        frame_skip = 300
        while True:

            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue

                corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(numpy.array(frame.to_image()), dictionary)
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                image = cv2.aruco.drawDetectedMarkers(numpy.array(image), corners, ids)
                # 読み込んだ画像の高さと幅を取得
                height = int(image.shape[0]/2)
                width = int(Timage.shape[1]/2)
                resized_img = cv2.resize(image,(width,height))
                cv2.imshow('Original', resized_img)
                # cv2.waitKey(1)
                frame_skip = int((time.time() - start_time)/frame.time_base)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
