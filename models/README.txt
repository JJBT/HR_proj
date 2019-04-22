Модели, в названии которых присутствует "_without_group",
обучались на данных с признаками:

# features = ['career', 'educ', 'has_descr', 'it_descr',
#             'it_post_count', 'it_post_prop',
#             'post_count', 'site', 'tight_post', 'y']

точность Логистической регрессии (logit): 68.13 %
точность SGD классификатора (SGDClassifier): 66.57 %
точность Случайного леса (RandomForest): 84.27 %

Модели, в названии которых отсутствует "_without_group",
обучались на данных с признаками:

# features = ['career', 'educ', 'has_descr', 'it_descr', 'group_count',
#             'it_group_count', 'it_group_prop', 'it_post_count', 'it_post_prop',
#             'post_count', 'site', 'tight_post', 'y', 'tight_group']

точность Логистической регрессии (logit): 90.65 %
точность SGD классификатора (SGDClassifier): 90.00 %
точность Случайного леса (RandomForest):  93.20%
