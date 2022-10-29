import numpy as np

import pandas as pd
import geopandas
import matplotlib.pyplot as plt

# excel_path = 'data/essd_ghg_data.xlsx'
# df = pd.read_excel(excel_path, sheet_name='data', usecols="A,C,F")
df = pd.read_csv('data/emission_by_countries.csv')
# add columns
df['value1'] = df['value']
df['value2'] = df['value']
select_first = lambda x: x.iloc[0]


def agg(min, max):
    def decade_agg(series):
        sub_df = df.loc[series.index]
        return sub_df[np.logical_and(sub_df['year'] > min, sub_df['year'] <= max)]['value'].mean()
    return decade_agg

df_pivot = pd.pivot_table(df, index=['ISO'], values=['country','value1', 'value2', ],
                          aggfunc={'value1': agg(1999, 2009), 'value2': agg(2009, 2019), 'country': select_first})
df_pivot['value'] = df_pivot['value2'] - df_pivot['value1']
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world.set_index('iso_a3', inplace=True)

cross = world.join(df_pivot)

# plot
fig, ax = plt.subplots(1, 1)
cross.plot(column='value', ax=ax,
           legend=False, cmap='OrRd',
           edgecolor='black',
           # scheme="quantiles",
           missing_kwds={
               "color": "lightgrey",
               "edgecolor": "red",
               "hatch": "///",
               "label": "Missing values",
           },
           )

plt.show()
