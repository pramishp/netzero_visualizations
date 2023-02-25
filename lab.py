import matplotlib.pyplot as plt
import numpy as np

# Define the data
energy_sources = ['a oil', 'b natural gas', 'c coal', 'd biomass', 'e nuclear',
                  'f hydro', 'g wind', 'h solar', 'i geothermal', 'j traditional biomass']

contrib_2020 = [20.42318778, 6.45602973, 50.6573167, 5.028050084, 1.572699935,
                6.561151583, 1.94650779, 0.866325649, 0.138979864, 6.349750885]

# Create the horizontal bar chart
fig, ax = plt.subplots()

# Set the x-axis and y-axis labels and title
ax.set_xlabel('Contribution (%)')
ax.set_ylabel('Energy Source')
ax.set_title('Energy Sources Contribution in 2020')

# Create the horizontal bars
bars = ax.barh(energy_sources, contrib_2020, color='skyblue')

# Add annotations to the bars
for i, bar in enumerate(bars):
    ax.annotate(f'{contrib_2020[i]:.2f}%', xy=(contrib_2020[i], i), va='center')

# Show the chart
plt.show()
