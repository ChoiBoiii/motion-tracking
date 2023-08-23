## IMPORT MODULES
import cv2
import numpy as np


# The processing for model 1 
def model_1(frame, prevFrame):
    return frame - prevFrame

# The processing for model 2
def model_2(frame, prevFrame):
    #return cv2.absdiff(frame, prevFrame)  # ANY DIFERENCE
    return cv2.subtract(frame, prevFrame)  # DIRECTIONAL

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

# The processing for model 5
def model_5(frame, prevFrame):

    ## CONSTANTS FOR OUTPUT MODIFICATION / CUSTOMISATION
    KERNEL = np.array([5])

    ## PROCESSING
    diff = cv2.subtract(frame, prevFrame)
    usedThresholdValue, diff = cv2.threshold(diff, None, None, cv2.THRESH_TOZERO | cv2.THRESH_TRIANGLE)
    diff = cv2.filter2D(diff, -1, kernel=KERNEL)

    ## RETURN
    return diff

# The processing for model 6
def model_6(frame, prevFrame):

    ## CONSTANTS FOR OUTPUT MODIFICATION / CUSTOMISATION
    #KERNEL = np.array([5])
    KERNEL = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])

    ## PROCESSING
    diff = cv2.absdiff(frame, prevFrame)
    usedThresholdValue, diff = cv2.threshold(diff, None, None, cv2.THRESH_TOZERO | cv2.THRESH_TRIANGLE)
    diff = cv2.filter2D(diff, -1, kernel=np.array([2]))
    diff = cv2.filter2D(diff, -1, kernel=KERNEL)

    ## RETURN
    return diff

# The processing for model 7
def model_7(frame, prevFrame):

    # Calculate absolute difference
    diff = cv2.absdiff(frame, prevFrame)

    # Attempt to filter out background noise
    usedThresholdValue, diff = cv2.threshold(diff, None, None, cv2.THRESH_TOZERO | cv2.THRESH_TRIANGLE)

    # Normalise from [0, maxPixelValue] -> [0, 255]
    maxPxVal = np.amax(diff)
    normalisingMultiplier = 255 / maxPxVal
    if normalisingMultiplier < 2:
        diff = cv2.filter2D(diff, -1, kernel=normalisingMultiplier) #KERNEL = np.array([normalisingMultiplier])
    
    # Print for debugging
    #print(usedThresholdValue, normalisingMultiplier)

    # Return
    return diff

# The processing for model 8
def model_8(frame, prevFrame, multiplierUseThreshold=2):

    # Calculate absolute difference
    diff = cv2.absdiff(frame, prevFrame)

    # Attempt to filter out background noise
    usedThresholdValue, diff = cv2.threshold(diff, None, None, cv2.THRESH_TOZERO | cv2.THRESH_TRIANGLE)

    # Normalise from [0, maxPixelValue] -> [0, 255]
    maxPxVal = np.amax(diff)
    if maxPxVal == 0:
        maxPxVal = 255
    normalisingMultiplier = 255 / maxPxVal
    if normalisingMultiplier > multiplierUseThreshold:
        normalisingMultiplier = multiplierUseThreshold
    diff = cv2.filter2D(diff, -1, kernel=normalisingMultiplier) #KERNEL = np.array([normalisingMultiplier])
    
    # Print for debugging
    #print(usedThresholdValue, normalisingMultiplier)

    # Return
    return diff

# The processing for model 9
def model_9(frame, prevFrame, multiplierUseThreshold=2):

    # Calculate absolute difference
    diff = cv2.absdiff(frame, prevFrame)

    # Attempt to filter out background noise
    usedThresholdValue, diff = cv2.threshold(diff, None, None, cv2.THRESH_TOZERO | cv2.THRESH_TRIANGLE)

    # Normalise from [0, maxPixelValue] -> [0, 255]
    maxPxVal = np.amax(diff)
    if maxPxVal == 0:
        maxPxVal = 255
    normalisingMultiplier = 255 / maxPxVal
    if normalisingMultiplier > multiplierUseThreshold:
        normalisingMultiplier = multiplierUseThreshold
    diff = cv2.filter2D(diff, -1, kernel=normalisingMultiplier) #KERNEL = np.array([normalisingMultiplier])
    
    # Print for debugging
    #print(usedThresholdValue, normalisingMultiplier)

    # Return
    return diff