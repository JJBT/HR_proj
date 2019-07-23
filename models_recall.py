# ОБУЧЕНИЕ
import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import accuracy_score, recall_score
from sklearn.ensemble import RandomForestClassifier

from meth_mod import save_model

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
df_label_0.reset_index(inplace=True, drop=True)

df = pd.concat([df_base, df_label_0, df_non,  df4, df5, df6, df7, df8, df9], ignore_index=True)
X, y = df.drop('y', axis=1).values, df['y'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.25)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=4)

forest = RandomForestClassifier(n_estimators=1000, n_jobs=-1)
params = {
    'max_depth': [x for x in range(3, 12)],
    'min_samples_split': [x for x in range(2, 6)],
    'min_samples_leaf': [x for x in range(1, 4)]
}

search = RandomizedSearchCV(estimator=forest, param_distributions=params, n_iter=50, scoring='recall', cv=cv)
print("TRAINING")
search.fit(X_train, y_train)
model = search.best_estimator_
print("BEST ESTIMATOR {}".format(model))

accuracy = recall_score(y_test, model.predict(X_test), average=None)
print(accuracy)

save_model(model_name='rf_fake_without_cw', model=model, accuracy=None, features=features)
