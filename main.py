from multiprocessing import Process, Barrier, Queue
from modules.capture import CaptureImage
from modules.process import ProcessImage
from modules.display import DisplayImage

def ready_capture_process(index, barrier):
    c = CaptureImage(index, barrier)
    p = ProcessImage(c.shared_array, c.size, c.lock, c.timestamp)

    return c, p, p.queue

def create_process(capture, process):
    p1 = Process(target=capture.capture)
    p2 = Process(target=process.extract)

    return p1, p2

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

    for process in process_lst:
        process.start()

    DisplayImage.displayAll(queue_lst, images_queue)

    # TODO: images_queue에 있는 이미지를 ai 처리하도록 만드는 코드 필요.

    for process in process_lst:
        process.join()
