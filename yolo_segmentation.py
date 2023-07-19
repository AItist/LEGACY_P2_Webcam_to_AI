#https://pysource.com/2023/02/21/yolo-v8-segmentation
from ultralytics import YOLO
import numpy as np
import time

class YOLOSegmentation:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, img):
        # Get img shape

        height, width, channels = img.shape
        
        # start = time.time()
        # results = self.model.predict(source=img.copy(), save=False, save_txt=False)
        # end = time.time()
        # print("time 11 :", end - start)

        # start = time.time()
        results = self.model.predict(source=img, save=False, save_txt=False)
        # end = time.time()
        # print("time 22 :", end - start)   # 3.1641645431518555 중요

        start = time.time()
        result = results[0]
        segmentation_contours_idx = []
        for seg in result.masks.segments:
            # contours
            seg[:, 0] *= width
            seg[:, 1] *= height
            segment = np.array(seg, dtype=np.int32)
            segmentation_contours_idx.append(segment)

        bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
        # Get class ids
        class_ids = np.array(result.boxes.cls.cpu(), dtype="int")
        # Get scores
        scores = np.array(result.boxes.conf.cpu(), dtype="float").round(2)
        # end = time.time()
        # print("time:", end - start)   # 0.001999378204345703

        return bboxes, class_ids, segmentation_contours_idx, scores