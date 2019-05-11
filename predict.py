import pickle
import pandas as pd

from sklearn.metrics import accuracy_score

path_to_df = "data/non_prog_parsed.xlsx"
df = pd.read_excel(path_to_df)

path_to_models = ['catbst', 'rf_new', 'rf_new1', 'rf_new', 'xgb_new', 'xgb_new1', 'xgb_new1_XY', 'xgb_new_XY']


features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_post_count', 'it_post_prop',
            'site', 'tight_post']
X = df.loc[:, features].values

for name in path_to_models:
    model = pickle.load(open(name, 'rb'))
    preds = model.predict(X)
    print('Model - ', name)
    print('Accuracy ', accuracy_score(df['y'].values, preds))
    print('\n')
# df['predict'] = preds
# df.to_excel(path_to_df)
# print(accuracy_score(df['y'].values, preds))

