import matplotlib.pyplot as plt
import numpy as np

# create some data
x = np.linspace(-np.pi, np.pi, 100)
y = np.sin(x)

# plot the data
fig, ax = plt.subplots()
ax.plot(x, y)

# annotate a point on the plot with an arrow
ax.annotate('Local Maximum', xy=(np.pi/2, 1), xytext=(np.pi/2+1, 0.5),
            arrowprops=dict(facecolor='red', shrink=0.05))

plt.show()
