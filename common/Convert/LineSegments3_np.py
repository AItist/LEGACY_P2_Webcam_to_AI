import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def closest_points_on_two_lines(line1, line2):
    u = line1[1] - line1[0]
    v = line2[1] - line2[0]
    w = line1[0] - line2[0]

    a = np.dot(u, u)
    b = np.dot(u, v)
    c = np.dot(v, v)
    d = np.dot(u, w)
    e = np.dot(v, w)
    D = a * c - b * b

    if D < 1e-6:
        sc = 0.0
        tc = d / b if b > c else e / c
    else:
        sc = (b * e - c * d) / D
        tc = (a * e - b * d) / D

    point_on_line1 = line1[0] + sc * u
    point_on_line2 = line2[0] + tc * v

    return point_on_line1, point_on_line2

def calculate_midpoints(lines):
    points = []
    
    _len = len(lines)

    if _len == 2:
        # print(f'***0')
        p1, p2 = closest_points_on_two_lines(lines[0], lines[1])
        mid_point = (p1 + p2) / 2
        points.append(mid_point)
    else:
        for i in range(_len):
            # print(f'***{i}')
            p1, p2 = closest_points_on_two_lines(lines[i], lines[(i+1)%len(lines)])
            mid_point = (p1 + p2) / 2
            points.append(mid_point)
            pass

    return points

def plot_lines_and_points(lines, points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for line in lines:
        ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], [line[0][2], line[1][2]])

    points = np.array(points)
    ax.scatter(points[:,0], points[:,1], points[:,2], color='r')

    plt.show()

def final_midpoint(midpoints):
    return np.round(np.sum(midpoints, axis=0) / len(midpoints), 3)

# example usage:
if __name__ == '__main__':
    line1 = np.array([[0,0,0], [1,1,1]])
    line2 = np.array([[0,1,0], [1,0,1]])
    line3 = np.array([[0,0,1], [1,1,0]])

    lines = [line1, line2, line3]
    print(line1.shape)

    points = calculate_midpoints(lines)
    # plot_lines_and_points(lines, points)

    print(final_midpoint(points))
    # print(np.sum(points, axis=0) / len(points))
