import device
import cv2

def get_all_webcams():
    """
    컴퓨터에 연결되어있는 모든 카메라를 가져온다.
    """
    # print OpenCV version
    print("OpenCV version: " + cv2.__version__)

    # Get camera list
    device_list = device.getDeviceList()
    index = 0

    output = {}

    for camera in device_list:
        # 웹캠의 리스트 프린트
        output[index] = camera[0]
        index += 1

    return output

def get_available_webcams(all_list):
    """
    모든 웹캠 리스트 중 지정된 웹캠의 지정 인덱스를 매칭한 딕셔너리를 반환한다.

    Parameters
    ----------
    all_list : dict

    Returns
    -------
    output : dict
    - key: 웹캠 인덱스
    - value: 서버 전달시 지정 웹캠 인덱스
    """
    output = {}
    # 0: 'Intel(R) RealSense(TM) Depth Camera 435 with RGB Module RGB' = 1
    # TODO : 환경변수 가져오도록 수정 리스트에 속한 웹캠만 사용하도록 수정
    checklist = {'Intel(R) RealSense(TM) Depth Camera 435 with RGB Module RGB' : 0,
                 'HD 4MP WEBCAM' : 0, # ABKO
                 'HD WEB CAMERA' : 1, # Home planet
                 'WCAM200': 2, # WCAM200
                 'HD-5M AutoFocus': 3} # Gcam

    for index, camera in all_list.items():
        cap = cv2.VideoCapture(index)

        if camera not in checklist:
            continue

        if cap.isOpened():
            output[index] = checklist[camera]

    return output

if __name__ == "__main__":
    result = get_all_webcams()

    print(result)

    result = get_available_webcams(result)

    print(result)