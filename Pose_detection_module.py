import cv2
import mediapipe as mp
import time

class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True, enable_segmentation=False, smooth_segmentation=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Defining variables
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.enable_segmentation, self.smooth_segmentation, self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True, hideImage=False, blur=(0, 0)):
        # Convert to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if hideImage:
            h, w, c = img.shape
            cv2.rectangle(img, (0, 0), (w, h), 0, cv2.FILLED)
        elif not blur == (0, 0):  # blur only if not set to imageless
            img = cv2.blur(img, blur)
        if draw:
            # If results are available
            if self.results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self, img, draw=False):
        lmList = []
        # If results are available
        if self.results.pose_landmarks:
            # for each landmark..
            for lm in self.results.pose_landmarks.landmark:
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
            return lmList