## IMPORT MODULES
import cv2
import numpy as np


# The processing for model 1 
def model_1(frame, prevFrame):
    return frame - prevFrame

# The processing for model 2
def model_2(frame, prevFrame):
    #return cv2.absdiff(frame, prevFrame)
    return cv2.subtract(frame, prevFrame)

# The processing for model 3
def model_3(frame, prevFrame, multiplier):
    diff = cv2.subtract(frame, prevFrame)
    out = cv2.filter2D(diff, -1, kernel=multiplier)
    return out

# The processing for model 4
def model_4(frame, prevFrame, THRESHOLD=30, MAX_VALUE=255):
    diff = cv2.subtract(frame, prevFrame)
    #diff = cv2.filter2D(diff, -1, kernel=np.array([20]))
    usedThresholdValue, diff = cv2.threshold(diff, THRESHOLD, MAX_VALUE, cv2.THRESH_BINARY)
    return diff
