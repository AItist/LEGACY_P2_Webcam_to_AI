
from common.enum_ import eSegs

def detect_seg(imgData, eSegs=eSegs.YOLO, debug=False):
    """
    이미지에서 사람을 검출한다.
    data[0] : index
    data[1] : ret
    data[2] : img
    ys : yolo_segmentation 객체

    return : 사람 검출된 이미지 / 검출된 사람이 없으면 None
    """

    if eSegs == eSegs.YOLO:
        import common.seg.yolo_ as yolo_
        return yolo_.detect_seg(imgData, debug=debug)

    """
    TODO: 새로운 사람 영역 인식 모델을 추가할 때마다 이곳에 추가해야 함.
    """

async def async_detect_seg(imgData, eSegs=eSegs.YOLO, debug=False):
    """
    이미지에서 사람을 검출한다.
    data[0] : index
    data[1] : ret
    data[2] : img
    ys : yolo_segmentation 객체

    return : 사람 검출된 이미지 / 검출된 사람이 없으면 None
    """

    if eSegs == eSegs.YOLO:
        import common.seg.yolo_ as yolo_
        return await yolo_.async_detect_seg(imgData, debug=debug)

    """
    TODO: 새로운 사람 영역 인식 모델을 추가할 때마다 이곳에 추가해야 함.
    """