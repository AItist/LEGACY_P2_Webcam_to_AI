from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def separate_coordinates(points):
    """Given a list of points, separate them into x, y, z coordinate lists."""
    x_values = points[:, 0]
    # x_values = [point[0] for point in points]
    y_values = points[:, 1]
    # y_values = [point[1] for point in points]
    z_values = points[:, 2]
    # z_values = [point[2] for point in points]
    return x_values, y_values, z_values

def draw_line(two_points, names):
    # 각 좌표를 각각의 리스트로 분리합니다.
    x_values, y_values, z_values = separate_coordinates(two_points)
    ax.plot(x_values, y_values, z_values)
    # 각 점에 표시를 추가합니다.
    ax.scatter(x_values, y_values, z_values, color='red')
    for i, txt in enumerate(names):
        ax.text(x_values[i], y_values[i], z_values[i], txt)
    pass

def md_draw_line(two_points, names):
    fig = plt.figure()

    # 3D 그래프를 그릴 준비를 합니다.
    ax = fig.add_subplot(111, projection='3d')

    # points = [(1, 3, 2), (4, 2, 5)]
    # names = ['Point 1', 'Point 2']

    draw_line(two_points, names)

    plt.show()
    pass

if __name__ == '__main__':    
    fig = plt.figure()

    # 3D 그래프를 그릴 준비를 합니다.
    ax = fig.add_subplot(111, projection='3d')

    points = np.array([np.array([1, 3, 2]), np.array([4, 2, 5])])
    names = ['Point 1', 'Point 2']

    print(type(points))
    draw_line(points, names)

    points = np.array([np.array([6, 7, 8]), np.array([9, 5, 4])])
    names = ['Point 3', 'Point 4']

    draw_line(points, names)

    plt.show()
