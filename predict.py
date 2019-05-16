import pickle
import pandas as pd
import json

from sklearn.metrics import accuracy_score

path_to_df = "data/java.xlsx"
df = pd.read_excel(path_to_df)
df = df.loc[:687, :]

models = ['rf', 'xgb_new_model']
path_to_models = list(map(lambda x: 'fited_full_data/' + x, models))


for name in path_to_models:

    with open(name + '_descr.json', 'r') as file:
        features = json.load(file)['features']

    X = df.loc[:, features].drop('y', axis=1).values

    model = pickle.load(open(name, 'rb'))
    preds = model.predict(X)
    df['{}_predict'.format(name)] = preds
# df['predict'] = preds
# df.to_excel(path_to_df)
# print(accuracy_score(df['y'].values, preds))
