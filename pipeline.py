import pandas as pd
from features import *
import xgboost as xgb
import pickle


df = pd.read_excel('test.xlsx')

links = df['link']
df['vk_id'] = df['link'].apply(lambda x: x.split('/')[-1])
df, err = main_loop(df, feature='id', func=get_id, ident='vk_id')
df, err = main_loop(df, feature='site', func=site)
df, err = main_loop(df, feature='career', func=career)
df, err = main_loop(df, feature='educ', func=educat)
df, err = main_loop(df, feature='user_descr', func=get_user_descr)
df, err = main_loop(df, feature='it_descr', func=it_descr)
df['has_descr'] = df['user_descr'].apply(lambda x: 1 if x != '' else 0)
df, err = main_loop(df, feature='group_count', func=group_count)
df, err = main_loop(df, feature='post_count', func=post_count)
df, err = main_loop(df, feature='it_post_count', func=it_post_count)

df = df.loc[:, ~df.columns.str.match('Unnamed')]

labels = ['site', 'career', 'educ', 'has_descr', 'it_descr', 'post_count', 'it_post_count', 'group_count']
df1 = df.loc[:, labels]

df1['tight_post'] = df1['post_count'].apply(lambda x: x if x <= 100 else 100)
df1['it_post_prop'] = df1['it_post_count'] / (df1['tight_post'] + 1)

model = 'models/' + 'logit_with_group_count'

with open(model, 'rb') as f:
    clf = pickle.load(f)

X = df1.values
y = clf.predict(X)
df1['y'] = y
df1['link'] = links
df1.to_excel('test.xlsx')
