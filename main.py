from multiprocessing import Process, Barrier, Queue, Lock
from modules.capture import CaptureImage
from modules.process import ProcessImage
from modules.display import DisplayImage
import cv2
import time
from queue import Empty
from threading import Thread, Lock

from concurrent.futures import ThreadPoolExecutor, wait
from common.data_ import data_unpack_process, data_package_process
from common.enum_ import ePoses, eSegs

import common.Convert.Transformation as Transformation
import common.Convert.StringToNumpy as StringToNumpy
import numpy as np
import websocket

CAM_COUNT = 4
isDebug = False
RUN_POSE = True # 포즈 검출 실행 여부
RUN_SEG = True # 영역 검출 실행 여부
poseFlag = ePoses.CVZONE # 포즈 검출 시행시 어떤 모듈을 사용할지 결정
segFlag = eSegs.YOLO # 영역 검출 시행시 어떤 모듈을 사용할지 결정

# Create a Lock
lock = Lock()

CAM_WIDTH = 640
CAM_HEIGHT = 480

camera1 = Transformation.Camera(position=np.array([0, 0, -1]), rotation=np.array([0, 0 , 0])) 
camera2 = Transformation.Camera(position=np.array([0.365, 0, -0.915]), rotation=np.array([0, -21.653, 0]))
camera3 = Transformation.Camera(position=np.array([0, 0, -1]), rotation=np.array([0, 0 , 0]))
camera4 = Transformation.Camera(position=np.array([0, 0, -1]), rotation=np.array([0, 0 , 0]))
cameras = [camera1, camera2, camera3, camera4]

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

        # print('1')
        return [pose_string, seg_img]
    except Exception as e:
        print(f"main/ai_model_inference: Error during model inference: {e}")
        pass

def _calculate_midpoints(poses):
    """
    calculate_midpoints에서 실행되는 카메라 2대 이상의 데이터 수집시 수행되는 함수
    각 카메라의 점들을 회전, 이동한 후 중점을 계산한다.
    각 두 선간의 중점 계산후 그 중점들의 중점을 계산한다.
    중점 배열을 문자열 변환한다.
    문자열을 반환한다.

    Parameters
    ----------
    poses : dict
    """
    pose_len = len(poses)
    

    result = {}
    try:
        # 문자열을 np.array로 변환
        # for camIndex, poseString in poses.items():
        for camIndex, poseString in enumerate(poses):
            _pose = StringToNumpy.convert_string_to_numpy_array(poseString, CAM_WIDTH, CAM_HEIGHT)
            result[camIndex] = _pose
        
        midpoint_result = None

        # 중점의 리스트를 생성한다.
        if pose_len == 1:
            midpoint_result = Transformation.set_midpoints_with_1camera(cameras, result)
        if pose_len == 2:
            midpoint_result = Transformation.set_midpoints_with_2cameras(cameras, result)
        elif pose_len == 3:
            midpoint_result = Transformation.set_midpoints_with_3cameras(cameras, result)
        elif pose_len == 4:
            midpoint_result = Transformation.set_midpoints_with_4cameras(cameras, result)

        # print(midpoint_result.shape)
        # print(midpoint_result[0])

        str_arr = ','.join(map(str, midpoint_result))
        # print(str_arr)

        return str_arr

        pass
    except Exception as e:
        # 'NoneType' object has no attribute 'split'
        # print(e)
        print('calculate_midpoints error')

    pass

# start = time.time()
def send_packet(packet):
    # Create a connection to the WebSocket server
    ws = websocket.WebSocket()

    # Connect to the server
    ws.connect("ws://localhost:8080")

    # Send the packet
    ws.send(packet)
    print('send complete')
    # global start
    # end = time.time()
    # print(f'time : {end - start}')
    # start = end

    # Close the connection
    ws.close()

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

                # continue

                try:
                    # print("AI model inference results:")
                    isPose = True
                    poses = []
                    segs = []
                    for i, future in enumerate(futures):
                        # results.append(future.result())
                        pose, seg = future.result()
                        if pose is None:
                            # print(f'{i} pose is none')
                            isPose = False
                            break

                        poses.append(pose)
                        segs.append(seg)
                        
                        # pose, seg = future.result()
                        # print(f"Camera {i+1}: pose {type(pose)} seg {type(seg)}")

                    # pose 데이터가 둘 이상 검출되었을 경우 (추가 연산 단계 진행가능)
                    if isPose:
                        # print('poses is not none')

                        # 포즈 리스트 가지고 추가 연산 진행
                        # 카메라 인스턴스 필요
                        packet_data = {}

                        # 포즈 데이터 가공
                        pose_midpoints = _calculate_midpoints(poses)
                        packet_data['pose_string'] = pose_midpoints
                        # print(f'pose_midpoints : {pose_midpoints}')

                        # 영역 데이터 가공
                        for i, seg in enumerate(segs):
                            packet_data[f'img_{i}'] = seg
                        # print(f'segs length : {len(segs)}')

                        packet = data_package_process(packet_data, CAM_COUNT)
                        # print(f'packet completed')

                        send_packet(packet)

                        pass
                    else:
                        # 포즈가 제대로 추정되지 못했다.
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
