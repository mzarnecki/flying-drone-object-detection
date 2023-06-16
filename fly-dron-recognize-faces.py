from djitellopy import Tello
from matplotlib import pyplot as plt
import cv2

def detect_face(image_source):
    # open image
    img = cv2.imread(image_source)

    # RGB and grayscale version
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # use predifined haar cascade filtersfrom OpenCV lib
    # https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    results = classifier.detectMultiScale(img_gray, minSize =(40, 40))

    if len(results) > 0:
        # iterate through all recognized objects 
        for (x, y, width, height) in results:
            # draw bounding box around recognized object
            cv2.rectangle(img_rgb, (x, y), (x + height, y + width), (0, 255, 0), 5)

    #plot picture
    plt.subplot(1, 1, 1)
    plt.imshow(img_rgb)
    plt.show()
    
    return results

    
#initialize drone and take off    
tello = Tello()
tello.connect()
tello.takeoff()
#go up to be on shoulders level (when starting from ground)
tello.move_up(50)

max_rotations = 10

for rotation in range(max_rotations):
    print(f"iteration {rotation} rotation\n")
    #rotate 1/10 of full circle at each step
    tello.rotate_counter_clockwise(36)
    #enable streaming
    tello.streamon()

    frame_read = tello.get_frame_read()
    cv2.imwrite("picture.jpg", frame_read.frame)
    image = "picture.jpg"
    results = detect_face(image)

    #when face detected do some manover and land
    if len(results) > 0:
        tello.move_back(50)
        tello.move_back(30)
        break

tello.land()