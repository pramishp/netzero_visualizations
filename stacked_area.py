
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.color_palette("mako", as_cmap=True)
#
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
sns.set_theme()
fig = plt.figure(figsize=(6.5, 3))
ax = plt.subplot(111)
# ax.margins(x=0)

ax.stackplot(df['Year'], *cols, labels=labels, edgecolor='white')


# draw vertical lines

for i, year in enumerate(df['Year']):
    interval = 5  # in years
    if year % interval == 0:
        ax.axvline(year, ls="--")
        denom = df['Year'][len(df) - 1] - df['Year'][0]
        start = (year - df['Year'][0]) / denom
        ax.text(
            start - 0.1,
            1.09,
            str(int(df.iloc[i].sum())) + "Gt",
            ha="left",
            va="top",
            weight="normal",
            fontsize="x-small",
            transform=ax.transAxes,
        )

        if i != 0:
            te1 = df[df["Year"] == year - interval].iloc[0].sum()
            te2 = df[df["Year"] == year].iloc[0].sum()
            change = (te2 - te1) / interval
            ax.text(
                start - 0.1,
                0.9,
                f"{change:.02f}\%/Yr",
                # ha="left",
                # va="top",
                weight="normal",
                fontsize="x-small",
                transform=ax.transAxes,
            )


# Put a legend
legend = plt.legend(frameon = 1)
frame = legend.get_frame()
plt.legend(facecolor='white', framealpha=0)
frame.set_edgecolor('red')

box = ax.get_position()
ax.set_position([box.x0, box.y0,
                 box.width * 0.8, box.height])

ax.legend(loc='upper center', bbox_to_anchor=(box.width + 0.44, 1),
          fancybox=False, shadow=False, ncol=1)

ax.set_ylabel(r"GHG Emissions (GT Co2 eq/yr) ")

plt.show()