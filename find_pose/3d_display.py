import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize variables
x, y = 2, 3
x_data, y_data = [x], [y]  # Store growing data

# Data generator function
def data_generator():
    global x, y
    while True:
        dx = np.random.rand() / 10
        dy = np.random.rand() / 10
        x += dx
        y += dy
        x_data.append(x)
        y_data.append(y)
        yield x_data, y_data  # Yield updated data

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(1.5, 3.5)
ax.set_ylim(2.5, 4.5)
line, = ax.plot([], [], "r-o")

# Update function (just updates the plot, no computation here)
def update(data):
    x_vals, y_vals = data  # Get updated data from generator
    line.set_data(x_vals, y_vals)
    return line,

# Create animation using the generator function
ani = FuncAnimation(fig, update, frames=data_generator, interval=200, repeat=False)

plt.show()
