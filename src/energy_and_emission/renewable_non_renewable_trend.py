from os.path import join
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Assuming the required modules and functions from constants and helpers.io are available
from constants import FIG_SINGLE_WIDTH, mm2inch
from helpers.io import save

sys.path.append("../")

plt.style.use('./styles/plot.mplstyle')

# File paths (assuming they exist in the specified directory)
rew_non_rew_spa1 = "./preprocessed_data/energy and emission/spa1_renewable_non_renewable_trend.csv"
rew_non_rew_ssp2 = "./preprocessed_data/energy and emission/ssp2_renewable_non_renewable_trend.csv"

df_spa1 = pd.read_csv(rew_non_rew_spa1, index_col=0)
df_spa1 = df_spa1[df_spa1['Year'] > 2000]
df_ssp2 = pd.read_csv(rew_non_rew_ssp2, index_col=0)
df_ssp2 = df_ssp2[df_ssp2['Year'] > 2000]


def plot():
    # Create a new figure
    fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, mm2inch(45)))

    # Add a new subplot to the figure
    ax = fig.add_subplot(111)
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    year = df_spa1['Year'].unique()
    line_ssp1_renewable, = ax.plot(year, df_spa1[df_spa1['fuel'] == 'renewable']['value'], label="SSP1 Renewable",
                                   color="limegreen")
    line_ssp1_nonrenewable, = ax.plot(year, df_spa1[df_spa1['fuel'] == 'non-renewable']['value'],
                                      label="SSP1 Non-Renewable", color="limegreen", linestyle="--")
    line_ssp2_renewable, = ax.plot(year, df_ssp2[df_ssp2['fuel'] == 'renewable']['value'], label="SSP2 Renewable",
                                   color="royalblue")
    line_ssp2_nonrenewable, = ax.plot(year, df_ssp2[df_ssp2['fuel'] == 'non-renewable']['value'],
                                      label="SSP2 Non-Renewable", color="royalblue", linestyle="--")

    plt.xlabel("Year")
    plt.ylabel("Energy (EJ)")

    # Create two legends
    legend1 = ax.legend(handles=[line_ssp1_renewable, line_ssp2_renewable], labels=["SSP1", "SSP2"], loc="upper left")
    ax.add_artist(legend1)

    # Add text annotations for "Renewable" and "Non-Renewable"
    ax.text(2020, 65, "Renewable", color="black", fontsize=4, ha="center", rotation=45)
    ax.text(2020, 180, "Non-Renewable", color="black", fontsize=4, ha="center", rotation=45)

    plt.tight_layout()
    save('renewable_non-renewable_trend')
    # plt.show()


plot()
