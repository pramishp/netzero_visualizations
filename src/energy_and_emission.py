from os.path import join
import os
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
if not os.path.exists(table_out_path):
    os.makedirs(table_out_path)
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
    bars1 = ax.bar(x - 0.3, v1, edgecolor='black', width=0.3,color='pink',linewidth=0.75)
    

    # Plot the second set of bars
    bars2 = ax.bar(x, v2, edgecolor='black', width=0.3, color='skyblue',linewidth=0.75)
    colors = ['#ADD8E6', '#FFFFE0']  # light blue and light yellow
    ax.set_prop_cycle(color=colors)

    # Calculate the percentage difference between the two bars for each x label
    diff_percentages = []
    for i in range(len(fuel)):
        diff = ((v2[i] - v1[i]) / v1[i]) * 100
        diff_percentages.append(diff)

    # Find the highest bar value between two for each x label
    highest_value = []
    for i in range(len(fuel)):
        highest_value.append(max(v1[i], v2[i]))

    # Add the percentage difference to the bar which is highest between two
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
                ax.text(bar2.get_x() + bar2.get_width() / 2, highest_value[i]+2,
                    '{:.2f}%'.format(diff_percentages[i]), ha='center', va='bottom', fontsize=5)
        
    # Add labels and titles
    # ax.set_xlabel('Fuel')
    ax.set_ylabel('Energy (EJ)', fontweight='bold', fontsize=7)
 
    ax.set_xticks(x-0.15)
    ax.set_xticklabels(fuel, rotation=90, fontweight='normal',fontsize='7')
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

    draw_stacked_barchart(fuel, values1, values2, legends=('SSP2', 'SSP1'))


#get_table()
draw_figure()