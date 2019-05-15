import pickle
from xgboost import XGBClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.model_selection import GridSearchCV, StratifiedKFold

from meth_mod import save_model

path_label0_xlsx = "data/id_label0_new.xlsx"
df_label_0 = pd.read_excel(path_label0_xlsx)

path_base1 = "data/Base1.xlsx"
df_base = pd.read_excel(path_base1)

path_non_prog = "data/non_prog_parsed.xlsx"
df_non = pd.read_excel(path_non_prog)

features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_group_count', 'it_post_count', 'it_post_prop',
            'site', 'y', 'weighted_group_sum']

df_base = df_base.loc[:, features]
df_base.reset_index(inplace=True, drop=True)

df_non = df_non.loc[:, features]
df_label_0 = df_label_0.loc[:, features]
df_label_0.reset_index(inplace=True, drop=True)

df = pd.concat([df_base, df_label_0, df_non], ignore_index=True)

X, y = df.drop('y', axis=1).values, df['y'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.25)

xgb = XGBClassifier()
# xgb.fit(X_train, y_train)
# print('Accuracy ', accuracy_score(y_test, xgb.predict(X_test)))

cv = StratifiedKFold(n_splits=5, shuffle=True)
param = {'n_estimators': [x for x in range(10, 251, 10)],
         'max_depth': [x for x in range(1, 7)]}

grid = GridSearchCV(xgb, param_grid=param, cv=cv, scoring='accuracy', verbose=1)
grid.fit(X_train, y_train)
model = grid.best_estimator_

accuracy = accuracy_score(y_test, grid.predict(X_test))
print(accuracy)

# save_model(model_name='xgb_new', model=model, accuracy=accuracy, features=features)
