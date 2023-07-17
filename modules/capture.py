import cv2
from multiprocessing import Array, Value, Lock
import time
import numpy as np

class CaptureImage:
    def __init__(self, index, barrier, capture_interval=1/60):
        self.env_capture_interval = capture_interval
        
        self.index = index
        self.barrier = barrier
        self.max_size = 1024 * 1024 * 3
        self.lock = Lock()
        self.shared_array = Array('B', self.max_size)
        self.size = Value('i', 0)

    def capture(self):
        cap = cv2.VideoCapture(self.index)

        # Use barrier to ensure cameras start at the same time
        self.barrier.wait()

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Write the gray image to shared memory
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()

            with self.lock:
                self.shared_array[:len(img_bytes)] = np.frombuffer(img_bytes, dtype='uint8')
                self.size.value = len(img_bytes)

            time.sleep(self.env_capture_interval)

        # When everything done, release the capture
        cap.release()
