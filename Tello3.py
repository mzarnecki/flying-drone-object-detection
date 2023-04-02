from djitellopy import Tello
import cv2

tello = Tello()

tello.connect()
tello.takeoff()
tello.move_left(30)
tello.rotate_counter_clockwise(90)
tello.streamon()
frame_read = tello.get_frame_read()
cv2.imwrite("picture.png", frame_read.frame)

tello.land()