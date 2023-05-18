import matplotlib.pyplot as plt
import numpy as np

# Generate some data for the plot
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create the figure and axes
fig, ax = plt.subplots()

# Plot the two lines
ax.plot(x, y1, label='Line 1')
ax.plot(x, y2, label='Line 2')

# Fill the area between the lines
ax.fill_between(x, y1, y2, where=(y1 >= y2), interpolate=True, alpha=0.5, color='green')
ax.fill_between(x, y1, y2, where=(y1 < y2), interpolate=True, alpha=0.5, color='red')

# Add labels, legend, and grid
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.legend()
ax.grid(True)

# Show the plot
plt.show()
