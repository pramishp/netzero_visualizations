import seaborn as sns
import matplotlib.pylab as plt
import numpy as np

# construct cmap
my_cmap = sns.light_palette("Navy", as_cmap=True)

N = 500
data1 = np.random.randn(N)
data2 = np.random.randn(N)
colors = np.linspace(0,1,N)
plt.scatter(data1, data2, c=colors, cmap=my_cmap)
plt.colorbar()
plt.show()