import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

path = "./data/Scopus_Data.csv"
df = pd.read_csv(path, encoding='unicode_escape')
df['count'] = [1 for _ in range(len(df))]
print(df.head())
print(df.columns)

df_pivot = pd.pivot_table(df, index=['Year'], values=['count'], aggfunc=np.sum)
# remove 2023 as it has only 1 paper of this date
df_pivot.drop(index=[2023], inplace=True)
print(df_pivot.head())

x, y = df_pivot.index, df_pivot.values.reshape(-1)
plt.plot(x, y)
plt.xlabel('Year')
plt.ylabel('Number of Published Research')
plt.show()