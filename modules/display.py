import cv2

class DisplayImage:
    @staticmethod
    def display(queue1, queue2):
        while True:
            img1 = queue1.get()  # Get image from queue
            img2 = queue2.get()  # Get image from queue

            if img1 is not None:
                cv2.imshow('frame1', img1)

            if img2 is not None:
                cv2.imshow('frame2', img2)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if Q is pressed
                break

    @staticmethod
    def displayAll(queues):
        while True:
            for i, queue in enumerate(queues):
                img = queue.get()
                if img is not None:
                    cv2.imshow(f'frame{i}', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if Q is pressed
                break
