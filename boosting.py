import numpy as np
import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

path_label0_xlsx = "data/label_data_0_out.xlsx"
df_label_0 = pd.read_excel(path_label0_xlsx)

path_base1 = "data/Base1_out.xlsx"
df_base = pd.read_excel(path_base1)

path_non_prog = "data/non_prog_parsed.xlsx"
df_non = pd.read_excel(path_non_prog)

features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_post_count', 'it_post_prop',
            'site', 'tight_post', 'y']

df_base = df_base.loc[:1000, features]
df_base.reset_index(inplace=True)
df_base = df_base.drop('index', axis=1)
df_non = df_non.loc[:, features]
df_label_0 = df_label_0.loc[:, features]

df = pd.concat([df_base, df_label_0, df_non])
X, y = df.drop('y', axis=1).values, df['y'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.25)

dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic', 'nthread': 4, 'eval_metric': 'auc'}
evallist = [(dtest, 'eval'), (dtrain, 'train')]
num_round = 20
bst = xgb.train(param, dtrain, num_round, evallist, early_stopping_rounds=10)
ypred = bst.predict(dtest, ntree_limit=bst.best_ntree_limit)
ypred = np.array([1 if x > 0.5 else 0 for x in ypred])
print(accuracy_score(y_test, ypred))
