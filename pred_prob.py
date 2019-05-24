import pandas as pd
import pickle
import json


path_label0_xlsx = "data/id_label0_new.xlsx"
df_label_0 = pd.read_excel(path_label0_xlsx)

path_base1 = "data/Base1.xlsx"
df_base = pd.read_excel(path_base1)

path_non_prog = "data/non_prog_parsed.xlsx"
df_non = pd.read_excel(path_non_prog)


df_base = df_base.loc[:1000, :]
df_base.reset_index(inplace=True, drop=True)
df_non = df_non.loc[:, :]


df = pd.concat([df_base, df_label_0, df_non], ignore_index=True)
# X, y = df.drop('y', axis=1).values, df['y'].values


path_to_models_prod = ['rf', 'xgb']

path_to_models_prod = list(map(lambda x: 'full/' + x, path_to_models_prod))
models = [pickle.load(open(name, 'rb')) for name in path_to_models_prod]


for name in path_to_models_prod:

    with open(name + '_descr.json', 'r') as file:
        features = json.load(file)['features']

    X = df.loc[:, features].drop('y', axis=1).values

    model = pickle.load(open(name, 'rb'))
    preds = model.predict(X)
    df[name + '_predict'] = preds
    probs = model.predict_proba(X)
    df[name + '_probas'] = probs[:, 1]
    print('\n')

df = df.loc[:, ~df.columns.str.match('Unnamed')]

