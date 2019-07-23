import pickle
from xgboost import XGBClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score

from sklearn.model_selection import GridSearchCV, StratifiedKFold

from meth_mod import save_model
import numpy as np

path_label0_xlsx = "data/id_labels0_new.xlsx"
df_label_0 = pd.read_excel(path_label0_xlsx)

path_base1 = "data/Base1.xlsx"
df_base = pd.read_excel(path_base1)

path_non_prog = "data/non_prog_parsed.xlsx"
df_non = pd.read_excel(path_non_prog)

df = pd.read_excel('data/V4-9.xlsx')

df4 = df[df['file'] == 4]
df8 = df[df['file'] == 8]
df9 = df[df['file'] == 9]
df4['y'] = 1
df8['y'] = 1
df9['y'] = 1
df4.reset_index(inplace=True, drop=True)
df8.reset_index(inplace=True, drop=True)
df9.reset_index(inplace=True, drop=True)

df5 = df[df['file'] == 5]
df6 = df[df['file'] == 6]
df7 = df[df['file'] == 7]
df5['y'] = 0
df6['y'] = 0
df7['y'] = 0
df5.reset_index(inplace=True, drop=True)
df6.reset_index(inplace=True, drop=True)
df7.reset_index(inplace=True, drop=True)

features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_group_count', 'it_post_count', 'it_post_prop',
            'site', 'y', 'weighted_group_sum']

df4 = df4.loc[:, features]
df5 = df5.loc[:, features]
df6 = df6.loc[:, features]
df7 = df7.loc[:, features]
df8 = df8.loc[:, features]
df9 = df9.loc[:, features]

df_base = df_base.loc[:, features]
df_base.reset_index(inplace=True, drop=True)

df_non = df_non.loc[:, features]
df_label_0 = df_label_0.loc[:, features]

df = pd.concat([df_base, df_label_0, df_non, df4, df5, df6, df7, df8, df9], ignore_index=True)

X, y = df.drop('y', axis=1).values, df['y'].values
weights = np.ones(X.shape[0])
weights[y == 1] = 1.5
X_train, X_test, y_train, y_test, weights_train, weights_test = train_test_split(X, y, weights, shuffle=True, test_size=0.25)

xgb = XGBClassifier()
# xgb_new_model.fit(X_train, y_train)
# print('Accuracy ', accuracy_score(y_test, xgb_new_model.predict(X_test)))

cv = StratifiedKFold(n_splits=5, shuffle=True)
param = {'n_estimators': [x for x in range(10, 51, 5)],
         'max_depth': [x for x in range(1, 5)]}

grid = GridSearchCV(xgb, param_grid=param, cv=cv, scoring='recall', verbose=1)
grid.fit(X_train, y_train, sample_weight=weights_train)
model = grid.best_estimator_

accuracy = recall_score(y_test, grid.predict(X_test), average=None)
print(accuracy)

save_model('xgb_recall', model, None, features)
