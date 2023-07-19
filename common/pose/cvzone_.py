import cv2
from cvzone.PoseModule import PoseDetector

detector = PoseDetector()

def detect_pose(imgdata, debug=False):
    
    img = detector.findPose(imgdata)
    lmList, bboxInfo = detector.findPosition(img)
    
    if bboxInfo:
        lmString = ''
        for lm in lmList:
            lmString += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'
        
        return lmString

    return None
