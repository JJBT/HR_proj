Модели, в названии которых присутствует "_without_group",
обучались на данных с признаками:

# features = ['career', 'educ', 'has_descr', 'it_descr',
#             'it_post_count', 'it_post_prop',
#             'post_count', 'site', 'tight_post', 'y', 'tight_group']

Точность моделей, обученных на этих признаках:
Логистическая регрессия - 82.57%
SGD классификатор - 82.43%
Случайный лес - 89.23%

Модели, в названии которых отсутствует "_without_group",
обучались на данных с признаками:

# features = ['career', 'educ', 'has_descr', 'it_descr', 'group_count',
#             'it_group_count', 'it_group_prop', 'it_post_count', 'it_post_prop',
#             'post_count', 'site', 'tight_post', 'y', 'tight_group']

Точность моделей:
Логистическая регрессия - 92.77%
SGD классификатор - 99.15%
Случайный лес - 99.85%
