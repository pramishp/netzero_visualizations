from os.path import join
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from constants import FIG_SINGLE_WIDTH, mm2inch

sys.path.append("../")

plt.style.use('./styles/plot.mplstyle')

# file paths
file_part = "./preprocessed_data/intro/emission_by_region_part_dev.csv"
file_no_part = "./preprocessed_data/intro/emission_by_region_no_part_dev.csv"


# columns : 'Units', 'region', 'fuel', 'value'

df_part = pd.read_csv(file_part)
df_no_part = pd.read_csv(file_no_part)

# aggregate value(sum) by fuel
df_part = pd.pivot_table(df_part, index=['Year'], values=['value'], aggfunc=np.sum)
df_no_part = pd.pivot_table(df_no_part, index=['Year'], values=['value'], aggfunc=np.sum)

# limit year to present
limit_year = 2015
df_limit = df_no_part[df_no_part.index <= limit_year]
lx, ly = df_limit.index.values, df_limit['value'].values

# filter dfpart and no part
df_part = df_part[df_part.index >= limit_year]
df_no_part = df_no_part[df_no_part.index >= limit_year]
x1, y1 = df_part.index.values, df_part['value'].values
x2, y2 = df_no_part.index.values, df_no_part['value'].values


def plot():
    spreading_factor = 3
    # create a new figure
    fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, mm2inch(60)))

    # add a new subplot to the figure
    ax = fig.add_subplot(111)
    # ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    ax.grid(axis='y')
    ax.spines['bottom'].set_position(('data', -2000))
    ax.spines['top'].set_position(('data', 12000))
    ax.spines['left'].set_bounds(low=-2000, high=12000)
    ax.spines['right'].set_bounds(low=-2000, high=12000)

    ax.plot(lx, ly, color='gray')
    ax.plot(x2, y2, label='w/o Participation', color='orange')

    ax.fill_between(x2, y2-100*spreading_factor, y2 + 100*spreading_factor,
                    color='orange', alpha=0.2, edgecolor='none')

    ax.plot(x1, y1, color='green', label='w Participation')
    ax.fill_between(x1, y1-100*spreading_factor, y1 + 100*spreading_factor,
                    color='green', alpha=0.2, edgecolor='none')

    ## add annotation
    # net zero at 2084.30
    net_zero_year = 2084.3

    ax.scatter(net_zero_year, 0, marker='o', alpha=0.5, s=5, color='green')
    # annotate a point on the plot with an arrow
    ax.annotate(' '*40, xy=(net_zero_year, 0), xytext=(net_zero_year + 5, 100),
                rotation=45,
                arrowprops=dict(facecolor='black',
                                linewidth=0.5,
                                arrowstyle='->,head_length=0.6,head_width=0.3')
                )
    ax.text(net_zero_year + 3, 700, "Net-Zero Reached", fontsize=4)

    ax.set_xlabel('Years')
    ax.set_ylabel('Emission in MtCO2')

    plt.legend()
    plt.show()

plot()