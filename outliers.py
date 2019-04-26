import pandas as pd
import numpy as np


df = pd.read_excel('data.xlsx')

labels = ['group_count', 'post_count', 'it_group_prop', 'it_post_prop']

filt_df = df.loc[:, labels]

low = 0.05
high = 0.95

quant_df = filt_df.quantile([low, high])

new_df = filt_df.apply(lambda x: x[x < quant_df.loc[high, x.name]], axis=0)

new_df = pd.concat([new_df, df.loc[:, list(set(df.columns) - set(labels))]], axis=1)
new_df.dropna(inplace=True)
new_df.reset_index(inplace=True, drop=True)
new_df.to_excel('data_out.xlsx')
