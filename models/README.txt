Модели, в названии которых присутствует "_without_group",
обучались на данных с признаками:

# features = ['career', 'educ', 'has_descr', 'it_descr',
#             'it_post_count', 'it_post_prop',
#             'post_count', 'site', 'tight_post', 'y']

Точность моделей, обученных на этих признаках:
Логистическая регрессия - 68.13%
SGD классификатор - 66.57%
Случайный лес - 84.27%

Модели, в названии которых отсутствует "_without_group",
обучались на данных с признаками:

# features = ['career', 'educ', 'has_descr', 'it_descr', 'group_count',
#             'it_group_count', 'it_group_prop', 'it_post_count', 'it_post_prop',
#             'post_count', 'site', 'tight_post', 'y', 'tight_group']

Точность моделей:
Логистическая регрессия - 90.65%
SGD классификатор - 90.00%
Случайный лес - 93.05%