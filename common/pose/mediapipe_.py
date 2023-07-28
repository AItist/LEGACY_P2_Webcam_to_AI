import asyncio
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.3)

def detect_pose(imgdata, debug=False):
    import cv2
    # await asyncio.sleep(0.005)

    # img = imgdata[2]
    img = imgdata

    results = pose.process(img)

    # mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # print(results.pose_landmarks)
    print(len(results.pose_landmarks.landmark))

    if debug:
        cv2.imwrite(f'webcam {imgdata[0]} pose.jpg', img)


    # XXX : Image 대신에 Pose position을 전달한다.
    return img_bgr


async def async_detect_pose(imgdata, debug=False):
    import cv2
    # await asyncio.sleep(0.005)

    img = imgdata[2]

    results = pose.process(img)

    # mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # print(results.pose_landmarks)
    print(len(results.pose_landmarks.landmark))

    if debug:
        cv2.imwrite(f'webcam {imgdata[0]} pose.jpg', img)


    # XXX : Image 대신에 Pose position을 전달한다.
    return img_bgr