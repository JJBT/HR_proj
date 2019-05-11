# ОБУЧЕНИЕ
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

path_label0_xlsx = "data/label_data_0.xlsx"
df_label_0 = pd.read_excel(path_label0_xlsx)

path_base1 = "data/Base1.xlsx"
df_base = pd.read_excel(path_base1)

path_non_prog = "data/non_prog_parsed.xlsx"
df_non = pd.read_excel(path_non_prog)

features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_group_count', 'it_post_count', 'it_post_prop',
            'site', 'tight_post', 'y']

df_base = df_base.loc[:1000, features]
df_base.reset_index(inplace=True, drop=True)
df_non = df_non.loc[:, features]
df_label_0 = df_label_0.loc[:, features]

df = pd.concat([df_base, df_label_0, df_non], ignore_index=True)
X, y = df.drop('y', axis=1).values, df['y'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.25)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=4)

forest = RandomForestClassifier(n_estimators=1000, class_weight={0: 1, 1: 0.5})
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
print(accuracy_score(y_test, model.predict(X_test)))

pickle.dump(model, open('rf_new', 'wb'))

with open('rf_new_descr.txt', 'w') as file:
    file.write('valid accuracy - {}\n'.format(accuracy_score(y_test, model.predict(X_test))))
    file.write('features = [{0}]\n'.format(','.join(features)))
    file.write('model - {0}'.format(model.__repr__()))
