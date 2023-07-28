import cv2
from multiprocessing import Array, Value, Lock
import time
import numpy as np

class CaptureImage:
    def __init__(self, index, barrier, capture_interval=1/60):
        self.env_capture_interval = capture_interval
        
        self.index = index
        self.barrier = barrier
        self.max_size = 480 * 640 * 3
        # self.max_size = 1024 * 1024 * 3
        self.lock = Lock()
        self.shared_array = Array('B', self.max_size)
        self.size = Value('i', 0)
        self.timestamp = Value('d', 0.0)  # Add timestamp

    def capture(self):
        cap = cv2.VideoCapture(self.index)

        # Use barrier to ensure cameras start at the same time
        self.barrier.wait() # 640, 480, 3
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # cv2.imwrite(f'frame{self.index}.jpg', frame)
            # print(frame.shape)

            # Write the gray image to shared memory
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()

            with self.lock:
                self.shared_array[:len(img_bytes)] = np.frombuffer(img_bytes, dtype='uint8')
                self.size.value = len(img_bytes)
                self.timestamp.value = time.time()  # Save the timestamp

            time.sleep(self.env_capture_interval)

        # When everything done, release the capture
        cap.release()
