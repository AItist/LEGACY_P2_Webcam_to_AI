

def data_unpack_process(data):
    """
    웹소켓으로 받은 데이터를 언팩
    """
    import base64
    import gzip
    import numpy as np

    index = data['index']
    ret = data['ret']
    compressed_frame = data['frame']

    decoded_frame = base64.b64decode(compressed_frame.encode('utf-8'))
    # print(decoded_frame)

    decompressed_frame = gzip.decompress(decoded_frame)
    # print(decompressed_frame)

    restored_frame = np.frombuffer(decompressed_frame, dtype=np.uint8)
    # print(restored_frame.shape)

    height, width, channels = 480, 640, 3
    reshaped_frame = np.reshape(restored_frame, (height, width, channels))
    # print(reshapd_frame.shape)

    data = [index, ret, reshaped_frame]

    return data

def data_package_process(data, cam_count):
    """
    가공이 끝난 데이터를 패키징
    """
    import json
    import gzip
    import base64

    data['cam_count'] = cam_count

    # print(f'after {data.keys()}')

    # for key, value in data.items():
    #     print('*****************')
    #     print(key, type(value))
    #     print('*****************')
    # pose_string <class 'str'>
    # img_0 <class 'numpy.ndarray'>
    # img_1 <class 'numpy.ndarray'>

    for key, value in data.items():
        if key == 'pose_string':
            pass

        if key == 'img_0' or key == 'img_1' or key == 'img_2' or key == 'img_3':
            # print(key)
            compressed_frame = gzip.compress(value)
            data[key] = base64.b64encode(compressed_frame).decode('utf-8')
        # print(key, type(value))

    # pose_string <class 'str'>
    # img_0 <class 'str'>
    # img_1 <class 'str'>

    # compressed_seg = gzip.compress(data[2])
    # # compressed_pose = gzip.compress(data[3])
    # compressed_pose = data[3]
    # # print(type(data[3]))
    # # print(compressed)

    """
    {
    'pose_string' : [포즈 문자열]
    'img_0' : [1번 카메라 이미지]
    'img_1' : [2번 카메라 이미지]
    'img_2' : [3번 카메라 이미지]
    'img_3' : [4번 카메라 이미지]
    }
    """

    json_data = json.dumps(data)
    return json_data

    # _data = 



    # _data = {
    #     'index': data[0],
    #     'ret': data[1],
    #     'frame': base64.b64encode(compressed_seg).decode('utf-8'),
    #     # 'poseframe': base64.b64encode(compressed_seg).decode('utf-8')
    #     'poseframe': compressed_pose
    #     # 'poseframe': base64.b64encode(compressed_pose).decode('utf-8')
    # }

    # json_data = json.dumps(_data)
    # return json_data