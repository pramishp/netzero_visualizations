import matplotlib.pyplot as plt
import numpy as np

# Data for the bars
categories = ['Category 1', 'Category 2', 'Category 3']
values1 = [20, 30, 10]
values2 = [40, 15, 25]
values3 = [10, 35, 20]

# Create an array for the x positions of the bars
x = np.arange(len(categories))

# Plot the bars
plt.bar(x, values1, label='Value 1')
plt.bar(x, values2, bottom=values1, label='Value 2')
plt.bar(x, values3, bottom=np.add(values1, values2), label='Value 3')

# Add labels and title
plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Stacked Bar Chart')

# Customize the x-axis tick labels
plt.xticks(x, categories)

# Add a legend
plt.legend()

# Display the plot
plt.show()
