import cv2
import numpy as np

baseline = 6 # horizontal distance between cameras in sentimiters
focal_length = 0.26

class Cameras:
    
    left_camera = None
    right_camera = None
    stereo = None
    face_cascade = None


    def __init__(self, cam1=0, cam2=1) -> None:
    # Camera streams 
        self.left_camera = cv2.VideoCapture(cam1) 
        self.right_camera = cv2.VideoCapture(cam2)

    def setup(self):
        # Stereo vision setup
        self.stereo = cv2.StereoSGBM_create() 
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Capture calibration data from cameras 
        ret, frame1 = self.left_camera.read()
        ret, frame2 = self.right_camera.read()

        # Find chessboard corners 
        ret1, corners1 = cv2.findChessboardCorners(frame1, (7,6))  
        ret2, corners2 = cv2.findChessboardCorners(frame2, (7,6))

        # Calibrate cameras
        ret, _, _, _, _ = cv2.calibrateCamera(
            [corners1, corners2],
            [(frame1.shape[1], frame1.shape[0]), 
            (frame2.shape[1], frame2.shape[0])],
            None, None
        )

def count_distance(self)-> int :
    ret, left_frame = self.left_camera.read() 
    ret, right_frame = self.right_camera.read()
    
    # Get disparity map from stereo vision 
    disparity = self.stereo.compute(left_frame, right_frame)  
    
    # Find pixels with valid disparity values
    non_zero_pixels = disparity[disparity > 0] 
    
    # Distance calculation 
    distance = (baseline * focal_length) / non_zero_pixels  

    # Print distance value 
    print(distance)

    return distance

def detect_faces(self)-> list:

    ret, img = self.left_camera.read()
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces 
    faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Print coordinates 
    for (x,y,w,h) in faces:
        print(x,y,w,h)

    return faces