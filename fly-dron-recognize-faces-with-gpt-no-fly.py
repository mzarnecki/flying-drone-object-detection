from djitellopy import Tello
import matplotlib
from matplotlib import pyplot as plt
import cv2
import sys
import base64
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import time

load_dotenv(find_dotenv())

matplotlib.use('TKAgg')

def detect_person(image_source):
    # open image
    with open(image_source, 'rb') as f:
        image = f.read()

        client = OpenAI()
        base64_image = base64.b64encode(image).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Check if image contains person. Respondwith only 1 if there is person on the image, 0 otherwise."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        },
                    },
                ],
            }],
        )

        return int(response.choices[0].message.content)

def show_image(imagePath):
    # plot picture
    img = cv2.imread(imagePath)
    # RGB and grayscale version
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.subplot(1, 1, 1)
    plt.imshow(img_rgb)
    plt.savefig('capture.png')
    plt.show(block=False) #avoid breaking program execution when image is displayed


#initialize drone and take off    
tello = Tello()
tello.connect()
# tello.takeoff()
#go up to be on shoulders level (when starting from ground)
# tello.move_up(50)

max_rotations = 10

for rotation in range(max_rotations):

    print(f"iteration {rotation} rotation\n")
    #rotate 1/10 of full circle at each step
    # tello.rotate_counter_clockwise(36)
    #enable streaming
    tello.streamon()

    frame_read = tello.get_frame_read()
    imagePath = "picture.jpg"
    cv2.imwrite(imagePath, frame_read.frame)
    result = detect_person(imagePath)
    print(f"result: {result}")
    time.sleep(2)

    #when face is detected, do some maneuver and land
    if result == 1:
        show_image(imagePath)
        print("person detected!!!, landing...")
        break

# tello.land()
plt.show()
sys.exit()
