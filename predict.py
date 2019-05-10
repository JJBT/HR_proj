import pickle
import pandas as pd

from sklearn.metrics import accuracy_score

path_to_df = "data/non_prog_parsed.xlsx"
df = pd.read_excel(path_to_df)

path_to_model = "models/forest_forest2"
model = pickle.load(open(path_to_model, 'rb'))

features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_post_count', 'it_post_prop',
            'site', 'tight_post', 'tight_group']
X = df.loc[:, features].values

preds = model.predict(X)
df['predict'] = preds
df.to_excel(path_to_df)

print(accuracy_score(df['y'].values, preds))

