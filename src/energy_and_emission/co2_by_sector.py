import copy

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.gridspec import GridSpec

from constants import FIG_DOUBLE_WIDTH, mm2inch
from helpers.io import save

plt.style.use('./styles/bar_stacked_sbs.mplstyle')

# Read data from CSV files
file_spa1 = "./preprocessed_data/energy and emission/spa1_co2_by_sector.csv"
file_ssp2 = "./preprocessed_data/energy and emission/spa2_co2_by_sector.csv"

df1 = pd.read_csv(file_spa1, index_col=0)
df1['region'] = df1['region'].replace('Africa_Western', 'Western Africa')
# df1 = df1[df1['region'] != "China"]
# df1 = df1[df1['region'] != "India"]
# df1 = df1[df1['sector'] != "building"]
df1 = df1[df1['sector'] != "agriculture"]

df2 = pd.read_csv(file_ssp2, index_col=0)
df2['region'] = df2['region'].replace('Africa_Western', 'Western Africa')

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
# regions = spa1_pivot.index.get_level_values(0).unique().tolist()[::-1]
regions = ['China', 'India', 'South Asia', 'Western Africa', 'Brazil']
years = spa1_pivot.index.get_level_values(1).unique().tolist()
colors = ['steelblue', 'khaki', 'lightseagreen', 'darksalmon', 'palegreen'][:len(spa1_pivot.columns)]
col2color = {col: color for col, color in zip(spa1_pivot.columns, colors)}

nrows = 2
ncols = 3
# fig, axs = plt.subplots(nrows, ncols, figsize=(12 * 2, 2 * 12), sharex=False)

fig = plt.figure(figsize=(FIG_DOUBLE_WIDTH, FIG_DOUBLE_WIDTH * 0.5))

# fig.suptitle('CO2 Emissions by Region and Year', fontsize=16)
gs = GridSpec(nrows=nrows, ncols=ncols * 2, figure=fig)
axs = []
# add subplots to get following layout:
#   |1|2|3|
#   | 4| 5|

ax1 = fig.add_subplot(gs[0, 0:2])
ax2 = fig.add_subplot(gs[0, 2:4])

ax3 = fig.add_subplot(gs[1, 0:2])
ax4 = fig.add_subplot(gs[1, 2:4])
ax5 = fig.add_subplot(gs[1, 4:6])
axs.append(ax1)
axs.append(ax2)
axs.append(ax3)
axs.append(ax4)
axs.append(ax5)

subplot_title = ['a', 'b', 'c', 'd', 'e']
# create plot
for i in range(len(axs)):
    ax = axs[i]
    index = i
    if index == len(regions):
        ax.set_visible(False)
        continue
    region = regions[i]
    sum_by_year1 = spa1_pivot.sum(axis=1)[region].values / 1000
    sum_by_year2 = ssp2_pivot.sum(axis=1)[region].values / 1000
    cols1 = []
    cols2 = []
    for j, col1 in enumerate(spa1_pivot.columns):
        cols1.append(
            {'label': col1, 'bottom': spa1_pivot.columns[:j], "values": spa1_pivot.loc[region][col1].values / 1000})
        cols2.append(
            {'label': col1, 'bottom': ssp2_pivot.columns[:j], "values": ssp2_pivot.loc[region][col1].values / 1000})

    # generate x-axis positions for each set of bars
    bar_width = 0.25
    x_pos2 = np.arange(len(years)) / 1.5  # division for controlling inter bar spaces in the x-axis
    x_pos1 = [x + bar_width for x in x_pos2]
    bottom1 = np.zeros((len(years)))
    bottom1_min = np.zeros((len(years)))
    bottom2 = np.zeros((len(years)))
    bottom2_min = np.zeros((len(years)))

    for l, col1 in enumerate(cols1):
        col2 = cols2[l]
        color = col2color[col1['label']]
        bottom_spa1 = np.where(col1['values'] > 0, bottom1, bottom1_min)
        bottom_ssp2 = np.where(col2['values'] > 0, bottom2, bottom2_min)
        bar_props1 = ax.bar(x_pos1, col1['values'], bottom=bottom_spa1, label=col1['label'], width=bar_width,
                            align='edge', color=color, edgecolor='black')
        bar_props2 = ax.bar(x_pos2, col2['values'], bottom=bottom_ssp2, label=col2['label'], width=bar_width,
                            align='edge', color=color, edgecolor='black')

        bottom1 += np.where(col1['values'] > 0, col1['values'], 0)
        bottom2 += np.where(col2['values'] > 0, col2['values'], 0)

        bottom1_min += np.where(col1['values'] < 0, col1['values'], 0)
        bottom2_min += np.where(col2['values'] < 0, col2['values'], 0)

        # Add percentage labels
        for m, rect in enumerate(bar_props1):
            height = rect.get_height()
            xpos = rect.get_x() + rect.get_width() / 2.0
            ypos = rect.get_y() + height / 2.0
            ratio = abs(col1['values'][m] / sum_by_year1[m])
            if ratio > 0.13:
                ax.text(xpos, ypos, '{:.1f}'.format(col1['values'][m]), ha='center', va='center', color='black',
                        fontweight='normal', fontsize=5)

        for m, rect in enumerate(bar_props2):
            height = rect.get_height()
            xpos = rect.get_x() + rect.get_width() / 2.0
            ypos = rect.get_y() + height / 2.0
            ratio = abs(col2['values'][m] / sum_by_year2[m])
            if ratio > 0.13:
                ax.text(xpos, ypos, '{:.1f}'.format(col2['values'][m]), ha='center', va='center', color='black',
                        fontweight='normal', fontsize=5)

    # Calculate the maximum value for the y-axis
    y_max = bottom2.max()
    y_min = bottom1_min.min()

    # Set y-axis limit
    ax.set_ylim([min(0, y_min), y_max * 1.2])
    xticks = np.asarray(x_pos1)
    xtick_labels = labels
    ax.set_xticks(xticks)
    ax.set_xticklabels(labels, fontweight='bold')

    ## minor labels
    xticks_minor = np.zeros((len(years) * 2))
    xticks_minor[range(0, 6, 2)] = x_pos2
    xticks_minor[range(1, 6, 2)] = x_pos1
    xticks_minor += + bar_width / 2

    minor_labels = ['BAU', 'OS'] * 3
    ax.set_xticks(xticks_minor, minor=True)
    ax.set_xticklabels(minor_labels, minor=True, fontsize='small')
    if y_min < 0:
        ax.spines['bottom'].set_visible(False)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.set_title(region)

    ax.set_ylabel('Emission (Gt CO2)', fontweight='bold')

    # give subplot a,b, c, d labels
    title = subplot_title[i]
    ax.text(-0.1, 1.1, title, transform=ax.transAxes, fontsize=7, fontweight='bold', va='top')

    # set x-axis label position for Brazil
    brazil_index = len(axs) - 1
    if i == brazil_index:
        tick_labels = ax.get_xticklabels()
        minor_tick_labels = ax.get_xticklabels(minor=True)
        for i, label in enumerate(tick_labels[:-1]):
            x, y = label.get_position()
            label.set_position((x, 0.15))
            # set minor
            index = i * 2
            m1, m2 = minor_tick_labels[index], minor_tick_labels[index + 1]
            mx1, my1 = m1.get_position()
            mx2, my2 = m2.get_position()
            m1.set_position((mx1, 0.15))
            m2.set_position((mx2, 0.15))

        # set SSP2 for 2080
        m = minor_tick_labels[-2]
        mx, my = m.get_position()
        m.set_position((mx, 0.15))


# Add custom legend
handles, labels = axs[0].get_legend_handles_labels()
nlabels = list(range(0, len(handles), 2))

# handle legend
fig.legend([handles[i] for i in nlabels][::-1],
           [labels[i].title() for i in nlabels][::-1],
           loc='center right', ncol=1,
           bbox_to_anchor=(0.8, 0.7))
plt.tight_layout()
# save('co2_by_sector')
plt.show()
