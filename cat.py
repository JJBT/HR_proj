import pickle
from catboost import CatBoostClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.model_selection import GridSearchCV, StratifiedKFold

path_label0_xlsx = "data/label_data_0.xlsx"
df_label_0 = pd.read_excel(path_label0_xlsx)

path_base1 = "data/Base1.xlsx"
df_base = pd.read_excel(path_base1)

path_non_prog = "data/non_prog_parsed.xlsx"
df_non = pd.read_excel(path_non_prog)

features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_group_count', 'it_post_count', 'it_post_prop',
            'site', 'y']

df_base = df_base.loc[:1000, features]
df_base.reset_index(inplace=True, drop=True)

df_non = df_non.loc[:, features]
df_label_0 = df_label_0.loc[:, features]

df = pd.concat([df_base, df_label_0, df_non], ignore_index=True)

X, y = df.drop('y', axis=1).values, df['y'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.25)

xgb = CatBoostClassifier()
# xgb_new_model.fit(X_train, y_train)
# print('Accuracy ', accuracy_score(y_test, xgb_new_model.predict(X_test)))

cv = StratifiedKFold(n_splits=5, shuffle=True)
param = {'n_estimators': [x for x in range(10, 201, 20)],
         'max_depth': [x for x in range(1, 5)]}

grid = GridSearchCV(xgb, param_grid=param, cv=cv, scoring='accuracy', verbose=1)
grid.fit(X_train, y_train)
model = grid.best_estimator_
print(accuracy_score(y_test, grid.predict(X_test)))

pickle.dump(model, open('xgb_new1', 'wb'))

with open('xgb_new1_descr.txt', 'w') as file:
    file.write('Data for fit - X, y')
    file.write('valid accuracy - {}\n'.format(accuracy_score(y_test, model.predict(X_test))))
    file.write('features = [{0}]\n'.format(','.join(features)))
    file.write('model - {0}'.format(model.__repr__()))
