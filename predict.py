import numpy as np
import pickle
import pandas as pd
import json

from sklearn.metrics import accuracy_score

path_to_df = "data/non_prog_parsed.xlsx"
df = pd.read_excel(path_to_df)

path_to_models = ['catbst', 'rf_new', 'rf_new1', 'xgb_new', 'xgb_new1', 'xgb_new1_XY', 'xgb_new_XY']
path_to_models = list(map(lambda x: 'models/' + x, path_to_models))

meta_data = []

for name in path_to_models:

    with open(name + '_descr.json', 'r') as file:
        features = json.load(file)['features']

    X = df.loc[:, features].drop('y', axis=1).values

    model = pickle.load(open(name, 'rb'))
    preds = model.predict(X)
    meta_data.append(preds)
    print('Model - ', name)
    print('Accuracy ', accuracy_score(df['y'].values, preds))
    print('\n')

"""ОБУЧИТЬ МЕТА АЛГОРИТМ НА МЕТА ДАННЫХ ДО ПРОДАКШНА"""
meta_data = np.array([meta_data])
META_ALGORITHM = pickle.load(open(path_to_models[1], 'rb'))
