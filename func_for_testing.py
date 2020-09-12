import pickle
import warnings
import pandas as pd
from sklearn.metrics import recall_score, accuracy_score
warnings.filterwarnings('ignore')
features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_group_count', 'it_post_count', 'it_post_prop',
            'site', 'y', 'weighted_group_sum']
features.remove('y')
model = pickle.load(open('full/xgb_recall', 'rb'))
# 4 8 9
df = pd.read_excel('data/V4-9.xlsx')

print('----1----')

df4 = df[df['file'] == 4]
df8 = df[df['file'] == 8]
df9 = df[df['file'] == 9]
df4['y'] = 1
df8['y'] = 1
df9['y'] = 1
df4.reset_index(inplace=True, drop=True)
df8.reset_index(inplace=True, drop=True)
df9.reset_index(inplace=True, drop=True)

dfs = [df4, df8, df9]

for train in dfs:
    print('Recall', recall_score(train['y'].values, model.predict(train.loc[:, features].values), average=None))

print('----0----')

df5 = df[df['file'] == 5]
df6 = df[df['file'] == 6]
df7 = df[df['file'] == 7]
df5['y'] = 0
df6['y'] = 0
df7['y'] = 0
df5.reset_index(inplace=True, drop=True)
df6.reset_index(inplace=True, drop=True)
df7.reset_index(inplace=True, drop=True)

dfs = [df5, df6, df7]

for train in dfs:
    print('Recall', recall_score(train['y'].values, model.predict(train.loc[:, features].values), average=None))
