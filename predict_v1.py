import json
import pandas as pd
import pickle
from meth_mod import predict

path_to_df = "data/V3.xlsx"
df = pd.read_excel(path_to_df)

path_to_models = ['rf', 'xgb']
path_to_models = list(map(lambda x: 'full/' + x, path_to_models))
models = [pickle.load(open(name, 'rb')) for name in path_to_models]

meta_data = pd.DataFrame()

for name in path_to_models:

    with open(name + '_descr.json', 'r') as file:
        features = json.load(file)['features']

    X = df.loc[:, features].drop('y', axis=1).values

    model = pickle.load(open(name, 'rb'))
    preds = predict(model, X)
    df[name + '_predict'] = preds

df.to_excel('data/V3_predict.xlsx')
