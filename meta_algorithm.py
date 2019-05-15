import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression

"""Data is metadata (predict of other models)"""
path_to_data = '...'
df = pd.read_excel(path_to_data)
X, y = df.drop('y', axis=1).values, df['y'].values

model = LogisticRegression()
model = model.fit(X, y)

pickle.dump(model, open('models/meta_algo', 'wb'))
