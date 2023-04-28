import matplotlib.pyplot as plt
import numpy as np

# Create the data
years = np.arange(2020, 2080, 5)
regions = ['China', 'India', 'South Asia', 'Europe', 'North America']
sectors = ['Transport', 'Industry', 'Buildings', 'Electricity', 'Agriculture']

ssp1_data = np.random.randint(100, 1000, (5, 12))  # SSP1 data
ssp2_data = np.random.randint(100, 1000, (5, 12))  # SSP2 data
spa1_data = np.random.randint(100, 1000, (5, 12))  # SPA1 data

# Create the stacked area chart
fig, axs = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(12, 6))

axs[0].stackplot(years, ssp2_data, labels=sectors)
axs[0].stackplot(years, spa1_data, labels=sectors)
axs[1].stackplot(years, ssp1_data, labels=sectors)
axs[1].stackplot(years, ssp2_data, labels=sectors)

# Add legend and labels
axs[0].legend(loc='upper left')
axs[1].legend(loc='upper left')
axs[0].set_xlabel('Year')
axs[1].set_xlabel('Year')
axs[0].set_ylabel('CO2 emissions')
axs[0].set_title('SSP2 vs SPA1')
axs[1].set_title('SSP1 vs SSP2')

# Show the plot
plt.show()
