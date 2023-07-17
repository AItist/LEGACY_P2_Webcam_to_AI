import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Create a new figure
fig = plt.figure()

# Create a 3D axis
ax = fig.add_subplot(111, projection='3d')

# Define the two points
point1, = ax.plot([], [], [], 'o', color='r')
point2, = ax.plot([], [], [], 'o', color='b')
line, = ax.plot([], [], [], color='g')

# Set the labels and the limits
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.set_zlim([0, 1])

# Function to generate two random points
def generate_points():
    p1 = np.random.rand(3)
    p2 = np.random.rand(3)
    return p1, p2

# Function to update the plot
def update(p1, p2):
    # Update the data for both points
    point1.set_data(p1[:2])
    point1.set_3d_properties(p1[2])
    point2.set_data(p2[:2])
    point2.set_3d_properties(p2[2])

    # Update the line data
    line.set_data([p1[0], p2[0]], [p1[1], p2[1]])
    line.set_3d_properties([p1[2], p2[2]])

    # Redraw the figure
    plt.draw()
    plt.pause(0.01)

# Generate points and update the plot in a loop
while True:
    p1, p2 = generate_points()
    update(p1, p2)
