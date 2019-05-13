import pandas as pd

df = pd.read_excel('err.xlsx')
print(df)

df_base = pd.read_excel('data/Base1.xlsx')

df_base.drop(df['weighted_group_sum'].values, axis=0, inplace=True)

df_base.to_excel('data/Base1.xlsx')

