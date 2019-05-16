import pickle
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score
from vecstack import stacking
from sklearn.linear_model import LogisticRegression

path_label0_xlsx = "~/PycharmProjects/tinkof/data/id_label0_new.xlsx"
df_label_0 = pd.read_excel(path_label0_xlsx)

path_base1 = "~/PycharmProjects/tinkof/data/Base1.xlsx"
df_base = pd.read_excel(path_base1)

path_non_prog = "~/PycharmProjects/tinkof/data/non_prog_parsed.xlsx"
df_non = pd.read_excel(path_non_prog)

features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_group_count', 'it_post_count', 'it_post_prop',
            'site', 'y', 'weighted_group_sum']

path_to_models = ['rf', 'xgb_new_model', 'xgb', 'xgb_new']
path_to_models = list(map(lambda x: 'full/' + x, path_to_models))
models = [pickle.load(open(name, 'rb')) for name in path_to_models]

df_base = df_base.loc[:, features]
df_base.reset_index(inplace=True, drop=True)

df_non = df_non.loc[:, features]
df_label_0 = df_label_0.loc[:, features]
df_label_0.reset_index(inplace=True, drop=True)

df = pd.concat([df_base, df_label_0, df_non], ignore_index=True)
X, y = df.drop('y', axis=1).values, df['y'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.25)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=4)
S_train, S_test = stacking(models, X_train, y_train, X_test,
                           regression=False,
                           mode='oof_pred_bag',
                           needs_proba=False,
                           save_dir=None,
                           metric=accuracy_score,
                           n_folds=5,
                           stratified=True,
                           shuffle=True,
                           verbose=2)
# for model in models:
#     model = model.fit(S_train, y_train)
#     y_pred = model.predict(S_test)
#     print('Accuracy: {}'.format(accuracy_score(y_test, y_pred)))

model = LogisticRegression()
model.fit(S_train, y_train)
print(accuracy_score(y_test, model.predict(S_test)))
