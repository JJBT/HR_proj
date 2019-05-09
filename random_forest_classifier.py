import pickle
import pandas as pd
import warnings
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

warnings.filterwarnings('ignore')

df = pd.read_excel('data.xlsx')
features = ['it_descr', 'it_group_prop', 'it_post_prop',
            'it_group_count', 'it_post_count', 'y']

df = df.loc[:, features]
X, y = df.drop('y', axis=1).values, df['y'].values

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.35,
                                                    shuffle=True,
                                                    random_state=42)
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


FOREST = RandomForestClassifier(n_estimators=fr.n_estimators,
                                max_depth=fr.max_depth,
                                min_samples_split=fr.min_samples_split,
                                min_samples_leaf=fr.min_samples_leaf)
FOREST.fit(X_train, y_train)
print(accuracy_score(y_test, FOREST.predict(X_test)))
