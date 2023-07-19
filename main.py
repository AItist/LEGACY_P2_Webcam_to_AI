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

isDebug = False
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
    from common.detect_pose import detect_pose
    from common.detect_seg import detect_seg

    try:
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

        return [pose_string, seg_img]
    except Exception as e:
        print(f"main/ai_model_inference: Error during model inference: {e}")
        pass

def process_images(images_queue: Queue):
    executor = ThreadPoolExecutor(max_workers=10)

    while True:
        if not images_queue.empty():
            images_list = None
            with lock:
                try:
                    for i in range(images_queue.qsize()):
                        images_list = images_queue.get()  
                        time.sleep(0.01)
                except Empty:
                    print('break')

            if images_list is not None:
                # print(f'timestamp : {images_list[-1]}')

                futures = [executor.submit(ai_model_inference, index, img) for index, img in enumerate(images_list[:-1])]
                wait(futures)

                try:
                    # print("AI model inference results:")
                    results = []
                    for i, future in enumerate(futures):
                        results.append(future.result())

                        # pose, seg = future.result()
                        # print(f"Camera {i+1}: pose {type(pose)} seg {type(seg)}")

                    isPose = True
                    poses = []
                    segs = []
                    for i, result in enumerate(results):
                        pose, seg = result
                        if pose is None:
                            print(f'{i} pose is none')
                            isPose = False
                            continue 
                        
                        poses.append(pose)
                        segs.append(seg)

                    # pose 데이터가 둘 이상 검출되었을 경우 (추가 연산 단계 진행가능)
                    if isPose:
                        # TODO: 내일 할것 
                        # 포즈 리스트 가지고 추가 연산 진행
                        # 카메라 인스턴스 필요
                        pass

                except Exception as e:
                    print(f"main/process_images: Error during AI model inference: {e}")
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
    images_queue = Queue()  

    for i in range(CAM_COUNT):
        capture, process, queue = ready_capture_process(i, barrier)
        capture_lst.append(capture)
        processimage_lst.append(process)
        queue_lst.append(queue)

        p1, p2 = create_process(capture, process)

        process_lst.append(p1)
        process_lst.append(p2)

    t3 = Thread(target=process_images, args=(images_queue,))
    threads_lst = [t3]

    for process in process_lst:
        process.start()

    for thread in threads_lst:
        thread.start()

    DisplayImage.generateAndDisplayAll(queue_lst, images_queue, lock)

    for process in process_lst:
        process.join()

    for thread in threads_lst:
        thread.join()
