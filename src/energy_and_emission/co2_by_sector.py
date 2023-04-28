import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read data from CSV files
file_spa1 = "../../preprocessed_data/energy and emission/spa1_co2_by_sector.csv"
file_ssp2 = "../../preprocessed_data/energy and emission/spa2_co2_by_sector.csv"

df1 = pd.read_csv(file_spa1, index_col=0)
# df1 = df1[df1['region'] != "China"]
# df1 = df1[df1['region'] != "India"]
df1 = df1[df1['sector'] != "building"]
df1 = df1[df1['sector'] != "agriculture"]

df2 = pd.read_csv(file_ssp2, index_col=0)
# df2 = df2[df2['region'] != "China"]
# df2 = df2[df2['region'] != "India"]
df2 = df2[df2['sector'] != "building"]
df2 = df2[df2['sector'] != "agriculture"]

regions = df1['region'].unique()
# define color palette
color_palette = sns.color_palette("husl", len(regions))

# regions
regions = pd.unique(df1['region'])
# define figure and subplots
fig, axs = plt.subplots(nrows=len(df1['sector'].unique()) // 2, ncols=2, figsize=(10, 10), sharex=True)
# fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 20))
# Define plot layout
# loop through sectors and plot lines for each region
for i, sector in enumerate(df1['sector'].unique()):
    sector_df1 = df1[df1['sector'] == sector]
    sector_df2 = df2[df2['sector'] == sector]
    col = i % 2
    ax = axs[i // 2, col]
    ax.set_yscale('log')

    # Set plot title and axis labels
    ax.set_title(sector)
    # ax.set_ylabel('CO2 emissions (MtCO2)')
    # plot lines for each region
    for j, region in enumerate(df1['region'].unique()):
        region_df1 = sector_df1[sector_df1['region'] == region]
        region_df2 = sector_df2[sector_df2['region'] == region]
        # plot solid line for ssp2
        ax.plot(region_df2['Year'], region_df2['value'], color=color_palette[j], label=region + ' ssp2')
        # plot dotted line for spa1
        ax.plot(region_df1['Year'], region_df1['value'], linestyle='dotted', color=color_palette[j],
                label=region + ' spa1')

# Set plot legend for region colors
handles = []
labels = []
for i, color in enumerate(color_palette):
    handles.append(plt.Rectangle((0, 0), 1, 1, color=color))
    labels.append(regions[i])
fig.legend(handles, labels, loc='lower center', ncol=len(color_palette))

# Set plot x-axis label
# axs[-1, 1].set_xlabel('Year')

# display the plot
plt.show()
