import copy

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.style.use('../../styles/bar_stacked_sbs.mplstyle')

# Read data from CSV files
file_spa1 = "../../preprocessed_data/energy and emission/spa1_co2_by_sector.csv"
file_ssp2 = "../../preprocessed_data/energy and emission/spa2_co2_by_sector.csv"

df1 = pd.read_csv(file_spa1, index_col=0)
# df1 = df1[df1['region'] != "China"]
# df1 = df1[df1['region'] != "India"]
# df1 = df1[df1['sector'] != "building"]
df1 = df1[df1['sector'] != "agriculture"]

df2 = pd.read_csv(file_ssp2, index_col=0)
# df2 = df2[df2['region'] != "China"]
# df2 = df2[df2['region'] != "India"]
# df2 = df2[df2['sector'] != "building"]
df2 = df2[df2['sector'] != "agriculture"]

regions = df1['region'].unique()
sectors = df1['sector'].unique()
# define color palette
color_palette = sns.color_palette("pastel", len(sectors))

years = [2030, 2050, 2080]
# regions
# regions = pd.unique(df1['region'])
# define figure and subplots
# fig, axs = plt.subplots(nrows=len(df1['region'].unique()) // 2 + 1, ncols=2, figsize=(10, 10), sharex=True)
# fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 20))
# Define plot layout

# process data
df1 = df1[(df1['Year'].isin(years))]
df2 = df2[(df2['Year'].isin(years))]

spa1_pivot = df1.pivot_table(index=['region', 'Year'], columns='sector', values='value', aggfunc='sum')
ssp2_pivot = df2.pivot_table(index=['region', 'Year'], columns='sector', values='value', aggfunc='sum')

#
labels = [str(year) for year in years]
regions = spa1_pivot.index.get_level_values(0).unique().tolist()
years = spa1_pivot.index.get_level_values(1).unique().tolist()
colors =  ['thistle','yellow','skyblue','pink', 'palegreen'][
         :len(spa1_pivot.columns)]
col2color = {col: color for col, color in zip(spa1_pivot.columns, colors)}

nrows = len(regions) / 2 if len(regions) % 2 == 0 else (len(regions) // 2 + 1)
ncols = 2
fig, axs = plt.subplots(nrows, ncols, figsize=(12 * 2, 2 * 12), sharex=False)
# fig.suptitle('CO2 Emissions by Region and Year', fontsize=16)

# create plot
for i in range(nrows):
    for k in range(ncols):
        ax = axs[i][k]
        index = i * 2 + k
        if index == len(regions):
            ax.set_visible(False)
            continue
        region = regions[i * 2 + k]
        cols1 = []
        cols2 = []
        for j, col1 in enumerate(spa1_pivot.columns):
            cols1.append(
                {'label': col1, 'bottom': spa1_pivot.columns[:j], "values": spa1_pivot.loc[region][col1].values})
            cols2.append(
                {'label': col1, 'bottom': ssp2_pivot.columns[:j], "values": ssp2_pivot.loc[region][col1].values})

        # generate x-axis positions for each set of bars
        bar_width = 0.4
        x_pos1 = np.arange(len(years))
        x_pos2 = [x + bar_width for x in x_pos1]
        bottom1 = np.zeros((len(years)))
        bottom1_min = np.zeros((len(years)))
        bottom2 = np.zeros((len(years)))
        bottom2_min = np.zeros((len(years)))

        for l, col1 in enumerate(cols1):
            col2 = cols2[l]
            color = col2color[col1['label']]
            bottom_spa1 = np.where(col1['values'] > 0, bottom1, bottom1_min)
            bottom_ssp2 = np.where(col2['values'] > 0, bottom2, bottom2_min)
            bar_props1 = ax.bar(x_pos2, col1['values'], bottom=bottom_spa1, label=col1['label'], width=bar_width,
                                align='edge', color=color, edgecolor='black')
            bar_props2 = ax.bar(x_pos1, col2['values'], bottom=bottom_ssp2, label=col2['label'], width=bar_width,
                                align='edge', color=color, edgecolor='black')

            # # add percentage
            # for j, xpos in enumerate(x_pos1):
            #     ax.text(xpos + bar_width / 2, bottom_spa1[j] + col1['values'][j] / 2,
            #             str(round(100 * col1['values'][j] / 100, 1)) + '%',
            #             ha='center', va='center', fontweight='bold', fontsize=15)
            #
            #     ax.text(x_pos2[j] + bar_width / 2, bottom_ssp2[j] + col2['values'][j] / 2,
            #             str(round(100 * col2['values'][j] / 100, 1)) + '%',
            #             ha='center', va='center', fontweight='bold', fontsize=15)

            bottom1 += np.where(col1['values'] > 0, col1['values'], 0)
            bottom2 += np.where(col2['values'] > 0, col2['values'], 0)

            bottom1_min += np.where(col1['values'] < 0, col1['values'], 0)
            bottom2_min += np.where(col2['values'] < 0, col2['values'], 0)

            # Add percentage labels
            # for i, rect in enumerate(bar_props1):
            #     height = rect.get_height()
            #     xpos = rect.get_x() + rect.get_width() / 2.0
            #     ypos = rect.get_y() + height / 2.0
            #     ax.text(xpos, ypos, '{:.1f}%'.format(height / 100 * 100), ha='center', va='center', color='white',
            #             fontweight='bold', fontsize=15)


            # for i, rect in enumerate(barprops):
            #     height = rect.get_height()
            #     xpos = rect.get_x() + rect.get_width() / 2.0
            #     ypos = rect.get_y() + height / 2.0
            #     ax.text(xpos, ypos, '{:.1f}%'.format(height / 100 * 100), ha='center', va='center', color='white',
            #             fontweight='bold', fontsize=15)

        # Calculate the maximum value for the y-axis
        y_max = bottom2.max()
        y_min = bottom1_min.min()

        # Set y-axis limit
        ax.set_ylim([min(0, y_min), y_max * 1.2])
        xticks = np.asarray(x_pos2) - 0.1
        xtick_labels = labels
        ax.set_xticks(xticks)
        ax.set_xticklabels(labels)
        ax.spines['bottom'].set_position('zero')
        ax.set_title(region)

# Add custom legend
handles, labels = axs[0, 0].get_legend_handles_labels()
nlabels = list(range(0, len(handles), 2))

# handle legend
box = axs[-1, -1].get_position()

fig.legend([handles[i] for i in nlabels][::-1],
           [labels[i] for i in nlabels][::-1],
           loc='center left', ncol=1,
           bbox_to_anchor=(box),
           fontsize=15,
           frameon=False)

plt.show()
