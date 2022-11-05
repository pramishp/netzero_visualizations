import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.transforms as transforms

sns.color_palette("mako", as_cmap=True)
#
plt.rcParams.update({
    # "text.usetex": True,
    "font.family": "Times New Roman"
})
plt.rcParams['legend.handlelength'] = 1
plt.rcParams['legend.handleheight'] = 1
plt.rcParams['legend.borderpad'] = 0.4
df = pd.read_excel('data/erlabee4esupp1.xlsx', sheet_name='Total regions')
df = pd.pivot_table(df, columns=['region_ar6_10'], aggfunc=np.sum)
df.drop("subsector", inplace=True)
df['Year'] = df.index.values.astype(int)
df.reset_index(drop=True, inplace=True)

# df = pd.read_csv("./data/emission_by_sector.csv", index_col=0, header=None).T
print(df.head())
print(df.columns)

cols = [df[col_name] for col_name in df.columns[:-1]]
labels = df.columns[:-1]

# plotting
# set seaborn style
# sns.set_theme()

fig = plt.figure(figsize=(6.5, 3),)
ax = plt.subplot(111)
trans = transforms.blended_transform_factory(
    ax.transData, ax.transAxes)


# make axis extend
ax.set_ylim([0, 80])
# ax.margins(x=0)
ax.stackplot(df['Year'], *cols, labels=labels, edgecolor='white')

# draw vertical lines

for i, year in enumerate(df['Year']):
    interval = 10  # in years
    if year % interval == 0:
        ax.axvline(year, ls="--", color='silver')
        denom = df['Year'][len(df) - 1] - df['Year'][0]
        start = (year - df['Year'][0]) / denom
        ax.text(
            year - int(interval / 4),  # start position in year
            1.02,  # y control
            str(int(df.iloc[i].sum())) + "Gt",
            ha="left",
            va="top",
            weight="bold",
            fontsize="9",
            transform=trans,
        )

        if i != 0:
            te1 = df[df["Year"] == year - interval].iloc[0].sum()
            te2 = df[df["Year"] == year].iloc[0].sum()
            change = (te2 - te1) / interval
            ax.text(
                year - int(interval) + 1,
                0.95,
                f"{change:.02f}\%/Yr",
                # ha="left",
                # va="top",
                weight="bold",
                fontsize="9",
                transform=trans,
            )
plt.xlabel('Year', fontname= 'Times New Roman', fontweight='bold', fontsize='12')
plt.ylabel('GHG emission (GT CO2 eq/yr)', fontname= 'Times New Roman', fontweight='bold', fontsize='12')
# Put a legend
box = ax.get_position()
ax.set_position([box.x0, box.y0,
                 box.width * 0.8, box.height])

# reverse the legend order and adjust position of legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1],
          loc='center left', bbox_to_anchor=(1, 0.5),
          fancybox=False, shadow=False, ncol=1, frameon=False,
          columnspacing=0, labelspacing=0.1, edgecolor='black')
ax.set_ylabel(r"GHG Emissions (GT Co2 eq/yr) ")

# hide top and right spines
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)


ax.set_ylabel(r"GHG Emissions (GT Co2 eq/yr) ")
# ax.set_xticks(df['Year'][::10])
# ax.set_yticks(list(range(80))[::10])
[t.set_color('red') for t in ax.yaxis.get_ticklines()]
plt.show()
