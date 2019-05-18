import pickle
import pandas as pd
import json
import warnings
from sklearn.metrics import accuracy_score

warnings.filterwarnings('ignore')

path_to_df = "data/id_label0_new.xlsx"
df = pd.read_excel(path_to_df)

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
    print(name, 'acc', accuracy_score(df['y'], preds))
    print('\n')
