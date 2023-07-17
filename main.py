from multiprocessing import Process, Barrier
from modules.capture import CaptureImage
from modules.process import ProcessImage
from modules.display import DisplayImage

def ready_capture_process(index, barrier):
    c = CaptureImage(index, barrier)
    p = ProcessImage(c.shared_array, c.size, c.lock)

    return c, p, p.queue

def create_process(capture, process):
    p1 = Process(target=capture.capture)
    p2 = Process(target=process.process)

    return p1, p2

if __name__ == '__main__':
    import modules.webcam_list as webcam_list
    
    webcam_lst = webcam_list.get_all_webcams()
    webcam_lst = webcam_list.get_available_webcams(webcam_lst)
    print(f'webcam_lst : {webcam_lst} / count : {len(webcam_lst)} ')
    CAM_COUNT = len(webcam_lst)
    
    # # TODO: CAM_COUNT 만큼 barrier 생성
    barrier = Barrier(CAM_COUNT)

    # # TODO: CAM_COUNT 만큼 capture, process, queue 생성
    capture_lst = []
    processimage_lst = []
    queue_lst = []
    process_lst = []

    for i in range(CAM_COUNT):
        capture, process, queue = ready_capture_process(i, barrier)
        capture_lst.append(capture)
        processimage_lst.append(process)
        queue_lst.append(queue)

        p1, p2 = create_process(capture, process)

        # print(type(p1))
        
        process_lst.append(p1)
        process_lst.append(p2)

    for process in process_lst:
        process.start()

    DisplayImage.displayAll(queue_lst)

    for process in process_lst:
        process.join()




    # # create a barrier for 2 processes (camera 1 and camera 2)
    # barrier = Barrier(2)

    # # instantiate capture, process and display objects
    # capture1, process1, queue1 = ready_capture_process(0, barrier)
    # capture2, process2, queue2 = ready_capture_process(1, barrier)

    # # create and start processes
    # p1, p2 = create_process(capture1, process1)
    # p3, p4 = create_process(capture2, process2)

    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()

    # # In the main process, we display the images
    # DisplayImage.display(queue1, queue2)

    # p1.join()
    # p2.join()
    # p3.join()
    # p4.join()
