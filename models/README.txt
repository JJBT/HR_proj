������, � �������� ������� ������������ "_without_group",
��������� �� ������ � ����������:

# features = ['career', 'educ', 'has_descr', 'it_descr',
#             'it_post_count', 'it_post_prop',
#             'post_count', 'site', 'tight_post', 'y']

�������� ������������� ��������� (logit): 68.13 %
�������� SGD �������������� (SGDClassifier): 66.57 %
�������� ���������� ���� (RandomForest): 84.27 %

������, � �������� ������� ����������� "_without_group",
��������� �� ������ � ����������:

# features = ['career', 'educ', 'has_descr', 'it_descr', 'group_count',
#             'it_group_count', 'it_group_prop', 'it_post_count', 'it_post_prop',
#             'post_count', 'site', 'tight_post', 'y', 'tight_group']

�������� ������������� ��������� (logit): 90.65 %
�������� SGD �������������� (SGDClassifier): 90.00 %
�������� ���������� ���� (RandomForest):  93.20%