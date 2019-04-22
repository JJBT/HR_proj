import pandas as pd
from features import *
import pickle


path_to_models1 = ['RandomForest_with_group_count', 'SGDClassifier_with_group_count', 'logit_with_group_count']
path_to_models1 = list(map(lambda x: 'models/' + x, path_to_models1))

path_to_models2 = ['RandomForest_without_group_count', 'SGDClassifier_without_group_count', 'logit_without_group_count']
path_to_models2 = list(map(lambda x: 'models/' + x, path_to_models2))

path_to_file = 'test.xlsx'
df = pd.read_excel(path_to_file)

links = df['link']
df['vk_id'] = df['link'].apply(lambda x: x.split('/')[-1])
df, err = main_loop(df, feature='id', func=get_id, ident='vk_id')
df['id'] = df['id'].astype('int')
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

labels1 = ['site', 'career', 'educ', 'has_descr', 'it_descr', 'post_count', 'it_post_count', 'group_count', 'it_group_count']
labels2 = ['site', 'career', 'educ', 'has_descr', 'it_descr', 'post_count', 'it_post_count', 'it_group_count']

#
# df1['tight_post'] = df1['post_count'].apply(lambda x: x if x <= 100 else 100)
# df1['it_post_prop'] = df1['it_post_count'] / (df1['tight_post'] + 1)
#

for i, path in enumerate(path_to_models1):
    with open(path, 'br') as f:
        clf = pickle.loads(f)
    X = df.loc[:, labels1].values
    y = clf.predict(X)
    df['model' + str(i)] = y


for i, path in enumerate(path_to_models2, 3):
    with open(path, 'br') as f:
        clf = pickle.loads(f)
    X = df[:, labels2].values
    y = clf.predict(X)
    df['model' + str(i)] = y

df.to_excel(path_to_file)

