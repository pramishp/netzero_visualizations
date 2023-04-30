import matplotlib.pyplot as plt
import numpy as np

# Example data
x = np.array(['A', 'B', 'C', 'D', 'E'])
y1 = np.array([1, -2, 3, -4, 5])
y2 = np.array([-2, 3, -1, 4, -3])

# Set up the figure and axes
fig, ax = plt.subplots()

# Plot the bars
ax.bar(x, y1, bottom=np.maximum(0, y2))
ax.bar(x, y2, bottom=np.minimum(0, y1))

# Set the y-axis label and tick labels
ax.set_ylabel('Value')
ax.set_yticks(np.arange(-6, 7, 2))

# Show the plot
plt.show()
