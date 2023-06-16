## DJI Ryze Tello flying drone object detection

### Description
This project presents autonomous flying drone which is taking off and rotating until it detects human face.
When face is detected, drone move up and back and then land.
As a drone DJi Ryze Tello Edu was used. Python API refenerence can be found under:
https://github.com/damiafuentes/DJITelloPy/blob/master/README.md

For face recognition haar cascade algorithm was chosen implemented in opencv lib
https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
example usage of haar cascade is shown in notebook face-recognition-with-haar-cascade.ipynb 

### Setup
`pip install -r requirements.txt`

### Run flying with face detection
`python fly-drone-recognize-faces.py`