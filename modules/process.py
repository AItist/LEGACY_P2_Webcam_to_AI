import cv2
from multiprocessing import Queue
from queue import Empty
import numpy as np
import time

class ProcessImage:
    def __init__(self, shared_array, size, lock, process_interval=0.1):
        self.env_process_interval = process_interval

        self.shared_array = shared_array
        self.size = size
        self.lock = lock
        self.queue = Queue()  # Queue for images

    def process(self):
        while True:
            try:
                with self.lock:
                    img_bytes = bytes(self.shared_array[:self.size.value])  # only read the number of bytes that were written

                if img_bytes:
                    img_np = np.frombuffer(img_bytes, dtype='uint8')
                    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

                    # Now img is a color OpenCV image
                    # Do processing here...

                    # Instead of showing the image here, we put it on the queue
                    while True:  # empty the queue and put the latest processed image
                        try:
                            self.queue.get_nowait()
                        except Empty:
                            break
                    self.queue.put(img)
            except Empty:
                pass

            time.sleep(self.env_process_interval)
