from os.path import join
import sys
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

sys.path.append("../")
from constants import FIG_SIZE, DISPLAY_DIP
from helpers.colors import set_stacked_area_colors

plt.style.use('../styles/bar_chart_style.mplstyle')

# out paths
table_out_path = "../results/tables"
# file paths
file_2050 = "../preprocessed_data/df2050_ene.csv"
file_2020 = "../preprocessed_data/df2020_ene.csv"

# columns : 'Units', 'region', 'fuel', 'value'

df_2050 = pd.read_csv(file_2050)
df_2020 = pd.read_csv(file_2020)

# aggregate value(sum) by fuel
fuel_by_value_2050 = pd.pivot_table(df_2050, index=['fuel'], values=['value'], aggfunc=np.sum)
fuel_by_value_2020 = pd.pivot_table(df_2020, index=['fuel'], values=['value'], aggfunc=np.sum)

'''
Sample output: 
                   value
fuel                    
a oil          49.337288
b natural gas  42.532221
c coal         34.211609
d biomass      67.806330
e nuclear      28.004743
'''


def get_table():
    cols = ['Energy Source', '2050 % contrib', '2020 % contrib']
    df = pd.DataFrame(columns=cols)
    for i, fuel in enumerate(pd.unique(fuel_by_value_2050.index)):
        # find percentage by each fuel
        contrib_2050 = (fuel_by_value_2050.loc[fuel].value / fuel_by_value_2050['value'].sum()) * 100
        contrib_2020 = (fuel_by_value_2020.loc[fuel].value / fuel_by_value_2020['value'].sum()) * 100
        new_row = [fuel, contrib_2050, contrib_2020]
        df.loc[i] = new_row


    df.to_csv(join(table_out_path, 'energy_sources and their contrib in 2050, 2020.csv'))


def draw_stacked_barchart(fuel, v1, v2, legends):
    # Set the X axis
    x = np.arange(len(fuel))

    # Create the figure and axis
    fig = plt.figure(figsize=FIG_SIZE, dpi=DISPLAY_DIP)
    ax = plt.subplot(111)
    # set color
    # TODO: make one for bar chart, option 4 looks good
    set_stacked_area_colors(ax, option_id=2)
    # Plot the first set of bars
    bars1 = ax.bar(x - 0.2, v1, edgecolor='black', width=0.2)

    # Plot the second set of bars
    bars2 = ax.bar(x, v2, edgecolor='black', width=0.2)

    # Add labels and titles
    # ax.set_xlabel('Fuel')
    ax.set_ylabel('Energy (in EJ)')
    ax.set_title('Fuel Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(fuel, rotation=45, ha='right')
    ax.legend((bars1[0], bars2[0]), legends)

    # Show the chart
    plt.tight_layout()
    plt.show()


def draw_figure():
    # Create a sample data
    fuel = pd.unique(fuel_by_value_2050.index)
    # fix labels

    fuel = [name[2:].title() for name in fuel]
    values1 = fuel_by_value_2020['value']
    values2 = fuel_by_value_2050['value']

    draw_stacked_barchart(fuel, values1, values2, legends=('SSP2', 'SPA1'))


# get_table()
draw_figure()