import pickle
import pandas as pd
import json
import warnings
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle

warnings.filterwarnings('ignore')

path_to_df = "data/id_label0_new.xlsx"
path_to_df1 = 'mckinsey_test.xlsx'

df = pd.read_excel(path_to_df)
df = df.loc[200:800, :]
df1 = pd.read_excel(path_to_df1)

df = pd.concat([df, df1], axis=0, ignore_index=True)
df = shuffle(df)
df.reset_index(inplace=True, drop=True)
df.drop('y', axis=1, inplace=True)

# df['y'] = 0

path_to_models = ['rf', 'xgb', 'xgb_new', 'xgb_new_model']
path_to_models_prod = ['rf', 'xgb']

path_to_models_prod = list(map(lambda x: 'full/' + x, path_to_models_prod))
models = [pickle.load(open(name, 'rb')) for name in path_to_models_prod]


for name in path_to_models_prod:

    with open(name + '_descr.json', 'r') as file:
        features = json.load(file)['features']

    X = df.loc[:, features].drop('y', axis=1).values

    model = pickle.load(open(name, 'rb'))
    preds = model.predict(X)
    df[name] = preds
    # print(name, 'acc', accuracy_score(df['y'], preds))
    print('\n')

df = df.loc[:, ~df.columns.str.match('Unnamed')]
df.to_excel('mckinsey_test_.xlsx')
