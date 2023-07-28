import numpy as np
import quaternion
import common.Convert.LineSegments3_np as line3

def rotation_matrix(rotations):
    """
    Returns the rotation matrix for rotations around the x, y, and z axes.
    """
    rx, ry, rz = np.radians(rotations)

    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(rx), -np.sin(rx)],
        [0, np.sin(rx), np.cos(rx)]
    ])

    Ry = np.array([
        [np.cos(ry), 0, np.sin(ry)],
        [0, 1, 0],
        [-np.sin(ry), 0, np.cos(ry)]
    ])

    Rz = np.array([
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz), np.cos(rz), 0],
        [0, 0, 1]
    ])

    # The rotation matrix for rotations about the x, y, and z axes
    R = np.dot(Rz, np.dot(Ry, Rx))

    return R

class Camera:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation # euler angle

    def rotation_matrix(rotations):
        """
        Returns the rotation matrix for rotations around the x, y, and z axes.
        """
        rx, ry, rz = np.radians(rotations)

        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(rx), -np.sin(rx)],
            [0, np.sin(rx), np.cos(rx)]
        ])

        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry)],
            [0, 1, 0],
            [-np.sin(ry), 0, np.cos(ry)]
        ])

        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0],
            [np.sin(rz), np.cos(rz), 0],
            [0, 0, 1]
        ])

        # The rotation matrix for rotations about the x, y, and z axes
        R = np.dot(Rz, np.dot(Ry, Rx))

        return R

    def rotate(self, point):
        """
        Returns the rotated point by the same amount as the camera rotation.
        """
        R = rotation_matrix(self.rotation)
        return np.dot(R, point)
    
    def translate(self, point):
        """
        Returns the translated point by the same amount as the camera position.
        """
        return point + self.position
    
    def transform(self, point):
        """
        Returns the transformed point by the same amount as the camera position and rotation.
        """
        return self.translate(self.rotate(point))
    
    def transform_points(self, points):
        """
        Returns the transformed points by the same amount as the camera position and rotation.
        """
        return np.array([self.transform(point) for point in points])
    
    def transform_points2(self, points):
        """
        Returns the transformed points by the same amount as the camera position and rotation.
        """
        results = np.array([])
        for point in points:
            results = np.append(results, self.transform(point))
        return results.reshape(-1, 3)

isReshape = False

def set_midpoints_with_1camera(cameras, points):
    transformed_points1 = cameras[0].transform_points(points[0])
    
    midpoint_result = transformed_points1.reshape([99])
    # # 카메라에 대응하는 변환된 좌표 배열을 생성한다.
    # new_array1 = [np.array([camera1.position, row]) for row in transformed_points1]

    return midpoint_result

def set_midpoints_with_2cameras(cameras, points):
    # print(points[0][0])
    # print(points[1][0])
    transformed_points1 = cameras[0].transform_points(points[0])
    transformed_points2 = cameras[1].transform_points(points[1])

    # print(transformed_points1[0])
    # print(transformed_points2[0])

    # 카메라에 대응하는 변환된 좌표 배열을 생성한다.
    new_array1 = [np.array([cameras[0].position, row]) for row in transformed_points1]
    new_array2 = [np.array([cameras[1].position, row]) for row in transformed_points2]

    midpoint_result = np.array([])
    for i, (a1, a2) in enumerate(zip(new_array1, new_array2)):
        # point_line1 = a1
        # point_line2 = a2
        # lines = [point_line1, point_line2]
        # points = line3.calculate_midpoints(lines)

        points = line3.calculate_midpoints([a1, a2])
        midpoint = line3.final_midpoint(points)

        midpoint_result = np.append(midpoint_result, midpoint)

    if isReshape:
        midpoint_result = midpoint_result.reshape(-1, 3)

    return midpoint_result

def set_midpoints_with_3cameras(cameras, points):
    transformed_points1 = cameras[0].transform_points(points[0])
    transformed_points2 = cameras[1].transform_points(points[1])
    transformed_points3 = cameras[2].transform_points(points[2])


    # 카메라에 대응하는 변환된 좌표 배열을 생성한다.
    new_array1 = [np.array([cameras[0].position, row]) for row in transformed_points1]
    new_array2 = [np.array([cameras[1].position, row]) for row in transformed_points2]
    new_array3 = [np.array([cameras[2].position, row]) for row in transformed_points3]

    midpoint_result = np.array([])
    for i, (a1, a2, a3) in enumerate(zip(new_array1, new_array2, new_array3)):
        # point_line1 = a1
        # point_line2 = a2
        # point_line3 = a3
        # lines = [point_line1, point_line2, point_line3]
        # points = line3.calculate_midpoints(lines)

        points = line3.calculate_midpoints([a1, a2, a3])
        midpoint = line3.final_midpoint(points)

        midpoint_result = np.append(midpoint_result, midpoint)

    if isReshape:
        midpoint_result = midpoint_result.reshape(-1, 3)
    # for i in midpoint_result:
    #     print(i)

    return midpoint_result

def set_midpoints_with_4cameras(cameras, points):
    transformed_points1 = cameras[0].transform_points(points[0])
    transformed_points2 = cameras[1].transform_points(points[1])
    transformed_points3 = cameras[2].transform_points(points[2])
    transformed_points4 = cameras[3].transform_points(points[3])


    # 카메라에 대응하는 변환된 좌표 배열을 생성한다.
    new_array1 = [np.array([cameras[0].position, row]) for row in transformed_points1]
    new_array2 = [np.array([cameras[1].position, row]) for row in transformed_points2]
    new_array3 = [np.array([cameras[2].position, row]) for row in transformed_points3]
    new_array4 = [np.array([cameras[3].position, row]) for row in transformed_points4]

    midpoint_result = np.array([])
    for i, (a1, a2, a3, a4) in enumerate(zip(new_array1, new_array2, new_array3, new_array4)):
        # point_line1 = a1
        # point_line2 = a2
        # point_line3 = a3
        # lines = [point_line1, point_line2, point_line3]
        # points = line3.calculate_midpoints(lines)

        points = line3.calculate_midpoints([a1, a2, a3, a4])
        midpoint = line3.final_midpoint(points)

        midpoint_result = np.append(midpoint_result, midpoint)

    if isReshape:
        midpoint_result = midpoint_result.reshape(-1, 3)
    # for i in midpoint_result:
    #     print(i)

    return midpoint_result
    

# XXX: 카메라 1개 기준 코드 수행
if __name__ == '__main__':
    # 1 카메라 클래스 기반 인스턴스 생성 (카메라 위치, 카메라 각도를 가짐)
    camera1 = Camera(position=np.array([1, 1, 1]), rotation=np.array([0, 0, 0]))

    # 2 각도와 위치를 변환할 점들의 리스트를 가져옵니다.
    point_positions = np.array([[1.28, 0.72, 1],
                            [1.28, -0.72, 1],
                            [-1.28, -0.72, 1],
                            [-1.28, 0.72, 1],])

    transformed_points = camera1.transform_points(point_positions)
    print(transformed_points)

    # transformed_points2 = camera1.transform_points2(point_positions)
    # print(transformed_points2)
