import matplotlib.pyplot as plt
import numpy as np

# create data for plots
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# create subplots with shared x-axis
fig, axs = plt.subplots(nrows=2, ncols=2)

# plot data in each subplot
axs[0,0].plot(x, y1)
axs[0,1].plot(x, y2)
axs[1,0].plot(x, y1)
axs[1,1].plot(x, y2)

# remove x-tick labels from top row
plt.setp(axs[0, :], xticks=[])

# add titles and axis labels
fig.suptitle('Subplots with Shared X-Axis')
axs[0, 0].set(title='Plot 1')
axs[0, 1].set(title='Plot 2')
axs[1, 0].set(title='Plot 3', xlabel='x-axis label')
axs[1, 1].set(title='Plot 4', xlabel='x-axis label')

plt.show()
