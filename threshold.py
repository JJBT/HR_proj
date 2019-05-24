import pandas as pd
from sklearn.metrics import accuracy_score
import numpy as np

df = pd.read_excel('full_train_df.xlsx')


def score_per_boundary(y_true, probas, thr):
    preds = probas.apply(lambda x: 1 if x > thr else 0)
    print('thr - {0}, acc - {1}'.format(thr, accuracy_score(y_true, preds)))


print('rf')
print('Default acc', accuracy_score(df['y'], df['full/rf_predict']))
for i in np.linspace(start=0, stop=1, num=10):
    score_per_boundary(df['y'], df['full/rf_probas'], i)


print('xgb')
print('Default acc', accuracy_score(df['y'], df['full/xgb_predict']))
for i in np.linspace(start=0, stop=1, num=10):
    score_per_boundary(df['y'], df['full/xgb_probas'], i)
