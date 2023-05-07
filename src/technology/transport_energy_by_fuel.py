import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read data from CSV files
import sys
sys.path.append("../../")
from constants import FIG_SIZE, DISPLAY_DIP
from helpers.colors import set_stacked_area_colors

plt.style.use('../../styles/stacked_area.mplstyle')
file_spa1 = "../../preprocessed_data/technology/spa1_transport_energy_by_fuel.csv"
file_ssp2 = "../../preprocessed_data/technology/ssp2_transport_energy_by_fuel.csv"
c,'pink', 'palegreen']
#sns.color_palolors = ['thistle','yellow','skyblue'ette("Set3", 5)

fig = plt.figure(figsize=FIG_SIZE, dpi=DISPLAY_DIP)

def get_transport_energy_by_fuel_chart(fuel_name, subplot_num):
    df1 = pd.read_csv(file_spa1, index_col=0)
    df1 = df1[df1['input'] == fuel_name]
    df2 = pd.read_csv(file_ssp2, index_col=0)
    df2 = df2[df2['input'] == fuel_name]


    ## format data in following str:

    '''
    Year Region1 Region2 ...
    2000 value1   value2 ...
    
    '''
    pt1 = pd.pivot_table(df1, index=['Year'], values='value', aggfunc=np.sum)
    pt1.reset_index(inplace=True)

    pt2 = pd.pivot_table(df2, index=['Year'], columns=['region'], values='value', aggfunc=np.sum)
    pt2.reset_index(inplace=True)

    pt3 =pd.pivot_table(df2, index=['Year'], values='value', aggfunc=np.sum)
    pt3.reset_index(inplace=True)


   
    # draw stacked area
    cols = [pt2[col_name] for col_name in pt2.columns[1:]]    
    labels = pt2.columns[1:]

    ax = plt.subplot(subplot_num)
    # set color
    set_stacked_area_colors(ax, option_id=2)

    ax.stackplot(pt2['Year'], *cols,
                 labels=labels,
                 edgecolor='white',
                 colors=colors,
                 alpha=1           
                 )
   

    ax.plot(pt1['Year'], pt1['value'], color='darkorange',linewidth=1.5, marker='.' )
    # draw plot at the uppermost surface of stacked area chart
    ax.plot(pt3['Year'], pt3['value'], color='seagreen',linewidth=1.5,marker='.' )
    if subplot_num == 121:
        ax.set_ylabel('Hydrogen (EJ)', fontweight= 'bold')
        ax.set_xlabel('Year', fontweight= 'bold')
        
        
    elif subplot_num == 122:
        ax.set_ylabel('Electricity (EJ)', fontweight= 'bold')
        ax.set_xlabel('Year', fontweight= 'bold')


    



hydrogren = "H2"
electricity = "Electricity"
get_transport_energy_by_fuel_chart(hydrogren, 121)
get_transport_energy_by_fuel_chart(electricity, 122)
plt.xlabel('Year',loc= 'center')
plt.legend(loc='lower center', bbox_to_anchor=(0.0000005, -0.2),ncol=5)

plt.show()
