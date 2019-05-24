import pickle
import pandas as pd
import json
import numpy as np

from sklearn.metrics import accuracy_score

path_to_df = "mckinsey_test_.xlsx"
df = pd.read_excel(path_to_df)
# df = df.loc[:687, :]

path_to_models = ['rf', 'xgb', 'xgb_new', 'xgb_new_model']
path_to_models = list(map(lambda x: 'full/' + x, path_to_models))
models = [pickle.load(open(name, 'rb')) for name in path_to_models]

meta_data = pd.DataFrame()

for name in path_to_models:

    with open(name + '_descr.json', 'r') as file:
        features = json.load(file)['features']

    X = df.loc[:, features].drop('y', axis=1).values

    model = pickle.load(open(name, 'rb'))
    preds = model.predict(X)
    meta_data['{}_predict'.format(name)] = preds

with open('full/Meta_model_descr.json', 'r') as file:
    # features = json.load(file)['features']
    # X = df.loc[:, features].values
    model = pickle.load(open('full/Meta_model', 'rb'))
    preds = model.predict(meta_data)
    print('acc: ', accuracy_score(np.zeros((preds.shape[0], 1)), preds))

# df = pd.read_excel('data/java_predict.xlsx')
df['Stacking_predict'] = preds
df.to_excel('mckinsey_test_.xlsx')


