import pandas as pd

df_arr = []

for i in range(4, 10):
    df = pd.read_excel('data/V.{}.xlsx'.format(i))
    df['file'] = i
    df_arr.append(df)

df = pd.concat(df_arr, axis=0, ignore_index=True)
df.to_excel('data/V4-9.xlsx')

