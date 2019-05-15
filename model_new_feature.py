# ОБУЧЕНИЕ
import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

from meth_mod import save_model

path_label0_xlsx = "data/id_labels0_new.xlsx"
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
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=4)

forest = RandomForestClassifier(n_estimators=1000)
params = {
    'max_depth': [x for x in range(3, 12)],
    'min_samples_split': [x for x in range(2, 6)],
    'min_samples_leaf': [x for x in range(1, 4)]
}

search = RandomizedSearchCV(estimator=forest, param_distributions=params, n_iter=50, scoring='accuracy', cv=cv)
print("TRAINING")
search.fit(X_train, y_train)
model = search.best_estimator_
print("BEST ESTIMATOR {}".format(model))

accuracy = accuracy_score(y_test, model.predict(X_test))
print(accuracy)

# save_model(model_name='rf_new_out', model=model, accuracy=accuracy, features=features)
