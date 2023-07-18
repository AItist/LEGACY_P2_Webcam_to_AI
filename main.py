from multiprocessing import Process, Barrier, Queue
from modules.capture import CaptureImage
from modules.process import ProcessImage
from modules.display import DisplayImage
import cv2
import time

from concurrent.futures import ThreadPoolExecutor, wait

def ready_capture_process(index, barrier):
    c = CaptureImage(index, barrier)
    p = ProcessImage(c.shared_array, c.size, c.lock, c.timestamp)

    return c, p, p.queue

def create_process(capture, process):
    p1 = Process(target=capture.capture)
    p2 = Process(target=process.extract)

    return p1, p2

def ai_model_inference(index, img, model):
    # TODO: Implement this function with your actual AI model
    # For example:
    # results = your_model.predict(img)
    # return results
    return f"{index} AI model inference results"

def process_images(images_queue: Queue):
    executor = ThreadPoolExecutor(max_workers=10)

    # model = YoloV5Model()  # TODO: Initialize your AI model here
    model = None

    while True:
        # print(images_queue)
        if not images_queue.empty():
            # Get the latest images list from the queue
            images_list = None
            while not images_queue.empty():
                images_list = images_queue.get()  # This will always get the last item if the queue is not empty

            if images_list is not None:
                futures = [executor.submit(ai_model_inference, index, img, model) for index, img in enumerate(images_list)]
                wait(futures)

                print("AI model inference results:")
                for i, furture in enumerate(futures):
                    result = furture.result()
                    print(f"Camera {i+1}: {result}")

        time.sleep(1/20)

if __name__ == '__main__':
    import modules.webcam_list as webcam_list
    
    webcam_lst = webcam_list.get_all_webcams()
    webcam_lst = webcam_list.get_available_webcams(webcam_lst)
    print(f'webcam_lst : {webcam_lst} / count : {len(webcam_lst)} ')
    CAM_COUNT = len(webcam_lst)
    
    barrier = Barrier(CAM_COUNT)

    capture_lst = []
    processimage_lst = []
    queue_lst = []
    process_lst = []
    images_queue = Queue()  # Queue for images list

    for i in range(CAM_COUNT):
        capture, process, queue = ready_capture_process(i, barrier)
        capture_lst.append(capture)
        processimage_lst.append(process)
        queue_lst.append(queue)

        p1, p2 = create_process(capture, process)

        process_lst.append(p1)
        process_lst.append(p2)

    # Start the process_images function as a separate process
    # TODO: images_queue에 있는 이미지를 ai 처리하도록 만드는 코드
    p3 = Process(target=process_images, args=(images_queue,))
    process_lst.append(p3)

    for process in process_lst:
        process.start()

    DisplayImage.generateAndDisplayAll(queue_lst, images_queue)


    for process in process_lst:
        process.join()
