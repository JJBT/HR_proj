import pickle
import pandas as pd
import warnings
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

warnings.filterwarnings('ignore')

df = pd.read_excel('data.xlsx')

features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_post_count', 'it_post_prop',
            'site', 'tight_post', 'y', 'tight_group']

df = df.loc[1320:, features]
X, y = df.drop('y', axis=1).values, df['y'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.35)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

params = {
    'n_estimators': [10, 20, 30, 40, 50, 60, 70],
    'max_depth': [x for x in range(3, 12)],
    'min_samples_split': [x for x in range(2, 6)],
    'min_samples_leaf': [x for x in range(1, 4)]
}
forest = RandomForestClassifier(oob_score=True)
search = RandomizedSearchCV(estimator=forest,
                            param_distributions=params,
                            n_iter=20,
                            scoring='accuracy',
                            random_state=42,
                            cv=cv)
search.fit(X_train, y_train)
fr = search.best_estimator_
print(accuracy_score(y_test, fr.predict(X_test)))
# s = pickle.dumps(cls)
FOREST = RandomForestClassifier(n_estimators=1500,
                                max_depth=fr.max_depth,
                                min_samples_split=fr.min_samples_split,
                                min_samples_leaf=fr.min_samples_leaf,
                                oob_score=True,
                                class_weight={0: 1, 1: 0.45})
FOREST.fit(X_train, y_train)
print(accuracy_score(y_test, FOREST.predict(X_test)))

df = pd.read_excel('data.xlsx')
features = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_post_count', 'it_post_prop',
            'site', 'tight_post', 'y', 'tight_group']

df = df.loc[1327:, features]
X, y = df.drop('y', axis=1).values, df['y'].values
print(accuracy_score(y, FOREST.predict(X)))
pr = FOREST.predict(X)
pr = pr.reshape(-1, 1)
s = pickle.dumps(FOREST)
with open('forest_2', 'wb') as f:
    f.write(s)
