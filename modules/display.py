import cv2
import time

class DisplayImage:
    @staticmethod
    def displayAll(queues, images_queue):
        while True:
            all_queues_have_data = all([not q.empty() for q in queues])
            if all_queues_have_data:
                images = []  # Initialize image list
                for i, queue in enumerate(queues):
                    # Get the latest image from the queue
                    img, timestamp = None, None
                    while not queue.empty():
                        img, timestamp = queue.get()  # This will always get the last item if the queue is not empty
                    
                    if img is not None:
                        images.append(img)  # Add image to the list
                        print(f"Timestamp for image from camera {i}: {timestamp}")
                        cv2.imshow(f'frame{i}', img)
                    else:
                        print(f"No image from camera {i}")

                # Now 'images' list contains the latest image from each webcam
                images_queue.put(images)  # Add the list to the queue

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if Q is pressed
                    break

            time.sleep(1/20)

