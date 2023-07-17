from multiprocessing import Process, Array, Value, Queue, Lock, Barrier
from queue import Empty
import cv2
import numpy as np
import time

def capture_image(shared_array, size, lock, index, barrier):
    cap = cv2.VideoCapture(index)

    # Use barrier to ensure cameras start at the same time
    barrier.wait()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Write the gray image to shared memory
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        with lock:
            shared_array[:len(img_bytes)] = np.frombuffer(img_bytes, dtype='uint8')
            size.value = len(img_bytes)

        time.sleep(0.1)

    # When everything done, release the capture
    cap.release()

def process_image(shared_array, size, lock, queue):
    while True:
        try:
            with lock:
                img_bytes = bytes(shared_array[:size.value])  # only read the number of bytes that were written

            if img_bytes:
                img_np = np.frombuffer(img_bytes, dtype='uint8')
                img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

                # Now img is a color OpenCV image
                # Do processing here...

                # Instead of showing the image here, we put it on the queue
                while True: # empty the queue and put the latest processed image
                    try:
                        queue.get_nowait()
                    except Empty:
                        break
                queue.put(img)
        except Empty:
            pass

        time.sleep(0.1)


def display_image(queue1, queue2):
    while True:
        img1 = queue1.get()  # Get image from queue
        img2 = queue2.get()  # Get image from queue
        # print(f'queue1 size: {queue1.qsize()}')
        # print(f'queue2 size: {queue2.qsize()}')

        if img1 is not None:
            # cv2.imwrite('test.jpg', img)
            cv2.imshow('frame1', img1)

        if img1 is not None:
            # cv2.imwrite('test.jpg', img)
            cv2.imshow('frame2', img2)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if Q is pressed
            break

_max_size = 1024 * 1024 * 3
_index = 0

def processing_main(max_size, index, barrier):
    lock = Lock()
    shared_array = Array('B', max_size)
    size = Value('i', 0)
    queue = Queue()  # Queue for images

    p1 = Process(target=capture_image, args=(shared_array, size, lock, index, barrier))
    p2 = Process(target=process_image, args=(shared_array, size, lock, queue))

    return p1, p2, queue


if __name__ == '__main__':
    # Maximum size for a JPEG image in bytes
    max_size = 1024 * 1024 * 3
    index = 0
    barrier = Barrier(2)

    p1, p2, queue1 = processing_main(max_size, index, barrier)
    p3, p4, queue2 = processing_main(max_size, index+1, barrier)

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    # In the main process, we display the images
    display_image(queue1, queue2)

    p1.join()
    p2.join()
    p3.join()
    p4.join()
