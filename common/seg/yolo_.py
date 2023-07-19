def yolo_instance():
    """
    yolo 인스턴스 생성
    """
    from yolo_segmentation import YOLOSegmentation

    ys = YOLOSegmentation("yolov8n-seg.pt")
    # ys = YOLOSegmentation("yolov8s-seg.pt")

    # ys.detect
    return ys

ys = yolo_instance()

def detect_seg(imgData, debug=False):
    import cv2
    import numpy as np
    # img = imgData[2]
    img = imgData

    # print(111)
    bboxes, classes, segmentations, scores = ys.detect(img)
    # print(222)  # 위에 detect되는 개체도 없으면 이 코드 라인이 실행이 안됨.

    count = 0
    for bbox, class_id, seg, score in zip(bboxes, classes, segmentations, scores):
        # print("bbox:", bbox, "class id:", class_id, "seg:", seg, "score:", score)

        # class id 0은 사람
        if class_id == 0:    
            count += 1
            (x, y, x2, y2) = bbox
            
            cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)

            cv2.polylines(img, [seg], True, (0, 0, 255), 4)

            cv2.putText(img, str(class_id), (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    
    # 사람 한번도 검출 안된거면 None 리턴
    if count == 0:
        return None

    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if debug:
        cv2.imwrite(f'webcam {imgData[0]} seg.jpg', img)
    return img_bgr
    # return img

async def async_detect_seg(imgData, debug=False):
    import cv2
    import numpy as np
    img = imgData[2]

    # print(111)
    bboxes, classes, segmentations, scores = ys.detect(img)
    # print(222)  # 위에 detect되는 개체도 없으면 이 코드 라인이 실행이 안됨.

    count = 0
    for bbox, class_id, seg, score in zip(bboxes, classes, segmentations, scores):
        # print("bbox:", bbox, "class id:", class_id, "seg:", seg, "score:", score)

        # class id 0은 사람
        if class_id == 0:    
            count += 1
            (x, y, x2, y2) = bbox
            
            cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)

            cv2.polylines(img, [seg], True, (0, 0, 255), 4)

            cv2.putText(img, str(class_id), (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    
    # 사람 한번도 검출 안된거면 None 리턴
    if count == 0:
        return None

    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if debug:
        cv2.imwrite(f'webcam {imgData[0]} seg.jpg', img)
    return img_bgr
    # return img