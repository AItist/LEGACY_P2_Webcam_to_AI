from multiprocessing import Process, Barrier, Queue, Lock
from modules.capture import CaptureImage
from modules.process import ProcessImage
from modules.display import DisplayImage
import cv2
import time
from queue import Empty
from threading import Thread, Lock

from concurrent.futures import ThreadPoolExecutor, wait
from common.enum_ import ePoses, eSegs

isDebug = True
RUN_POSE = True # 포즈 검출 실행 여부
RUN_SEG = True # 영역 검출 실행 여부
poseFlag = ePoses.CVZONE # 포즈 검출 시행시 어떤 모듈을 사용할지 결정
segFlag = eSegs.YOLO # 영역 검출 시행시 어떤 모듈을 사용할지 결정

# Create a Lock
lock = Lock()

def ready_capture_process(index, barrier):
    c = CaptureImage(index, barrier)
    p = ProcessImage(c.shared_array, c.size, c.lock, c.timestamp)

    return c, p, p.queue

def create_process(capture, process):
    p1 = Process(target=capture.capture)
    p2 = Process(target=process.extract)

    return p1, p2

def ai_model_inference(index, img):
    """
    AI 모델 추론 함수
    포즈와 영역 추론을 수행한다.
    
    Parameters
    ----------
    index : int
        카메라 인덱스
    img : numpy.ndarray
        이미지

    Returns
    -------
    pose_string : str
        포즈 문자열
    seg_img : numpy.ndarray
        영역 이미지
    """
    from common.detect_pose import detect_pose
    from common.detect_seg import detect_seg

    pose_string = None
    seg_img = None

    if RUN_POSE:
        pose_string = detect_pose(img, poseFlag)

    if RUN_SEG:
        seg_img = detect_seg(img, segFlag)
        seg_img = cv2.flip(seg_img, 0)

    if isDebug:
        print(f'{index} : {pose_string}')
        cv2.imwrite(f'seg_{index}.jpg', seg_img)
        pass

    return pose_string, seg_img
    # return f"{index} AI model inference results"

def process_images(images_queue: Queue):
    executor = ThreadPoolExecutor(max_workers=10)

    while True:
        if not images_queue.empty():
            # Get the latest images list from the queue
            images_list = None
            with lock:
                try:
                    for i in range(images_queue.qsize()):
                        images_list = images_queue.get()  # This will always get the last item if the queue is not empty
                        # print(i, images_queue.qsize(), images_queue.empty(), images_list[-1])
                        time.sleep(0.01)
                        pass 

                    # print(images_queue.qsize(), images_queue.empty(), images_list[-1])
                except Empty:
                    print('break')

            if images_list is not None:
                print(f'timestamp : {images_list[-1]}')

                futures = [executor.submit(ai_model_inference, index, img) for index, img in enumerate(images_list[:-1])]
                wait(futures)

                print("AI model inference results:")
                for i, future in enumerate(futures):
                    result = future.result()
                    print(f"Camera {i+1}: {result}")
                    pass

        time.sleep(1/5)

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
    # images_queue = manager.Queue()  # Queue for images list
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

    DisplayImage.generateAndDisplayAll(queue_lst, images_queue, lock)


    for process in process_lst:
        process.join()
