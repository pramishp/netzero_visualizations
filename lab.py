import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(10, 6))
gs = GridSpec(nrows=2, ncols=6, figure=fig)

# Access the axes in the first row and first column
ax1 = fig.add_subplot(gs[0, 0:2])
ax1.plot([1, 2, 3], [4, 5, 6])
ax1.set_title('First Plot')

# Access the axes in the first row and second column
ax2 = fig.add_subplot(gs[0, 2:4])
ax2.plot([1, 2, 3], [4, 2, 1])
ax2.set_title('Second Plot')

# Access the axes in the first row and third column
ax3 = fig.add_subplot(gs[0, 4:6])
ax3.plot([1, 2, 3], [3, 3, 3])
ax3.set_title('Third Plot')

# Access the axes in the second row and first column
ax4 = fig.add_subplot(gs[1, 0:3])
ax4.plot([1, 2, 3], [1, 2, 1])
ax4.set_title('Fourth Plot')

# Access the axes in the second row and second column
ax5 = fig.add_subplot(gs[1, 3:6])
ax5.plot([1, 2, 3], [5, 6, 5])
ax5.set_title('Fifth Plot')

plt.tight_layout()
plt.show()
