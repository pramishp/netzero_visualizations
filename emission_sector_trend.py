
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import matplotlib.transforms as transforms


sns.color_palette("mako", as_cmap=True)
# global params
plt.rcParams.update({
    # "text.usetex": True,
    "font.family": "Times New Roman"
})

df = pd.read_csv("./data/emission_by_sector.csv", index_col=0, header=None).T
df.reset_index(drop=True, inplace=True)
df.sort_values(['Year'])
print(df.head())
print(df.columns)

cols = [df[col_name] for col_name in df.columns[1:]]
labels = df.columns[1:]


# plotting
# set seaborn style
# sns.set_theme()

fig = plt.figure(figsize=(6.5, 3))
ax = plt.subplot(111)
# ax.margins(x=0)
trans = transforms.blended_transform_factory(
    ax.transData, ax.transAxes)

ax.stackplot(df['Year'], *cols, labels=labels, edgecolor='white')


# draw vertical lines

for i, year in enumerate(df['Year']):
    interval = 5  # in years
    if year % interval == 0:
        ax.axvline(year, ls="--", color='red')

        # total emission at top of vertical line
        ax.text(
            year - int(interval/4),  # start position in year
            1.09,  # y control
            str(int(df.iloc[i].sum())) + "Gt",
            ha="left",
            va="top",
            weight="normal",
            fontsize="x-small",
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
                weight="normal",
                fontsize="x-small",
                transform=trans,
            )


# Put a legend
legend = plt.legend(frameon=1)
frame = legend.get_frame()
plt.legend(facecolor='white', framealpha=0)
frame.set_edgecolor('red')

box = ax.get_position()
ax.set_position([box.x0, box.y0,
                 box.width * 0.8, box.height])

ax.legend(loc='upper center', bbox_to_anchor=(box.width + 0.44, 1),
          fancybox=False, shadow=False, ncol=1)

ax.set_ylabel(r"GHG Emissions (GT Co2 eq/yr) ")
# ax.set_xticks(df['Year'][::10])
# ax.set_yticks(list(range(80))[::10])
[t.set_color('red') for t in ax.yaxis.get_ticklines()]
plt.show()