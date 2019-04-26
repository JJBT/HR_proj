from features import *
import pickle


path_to_models1 = ['forest_forest1', 'forest_forest2']
path_to_models1 = list(map(lambda x: 'models/' + x, path_to_models1))

# path_to_models2 = ['sgd_without_group', 'logit_without_group']
# path_to_models2 = list(map(lambda x: 'models/' + x, path_to_models2))


# labels2 = ['site', 'career', 'educ', 'has_descr', 'it_descr', 'post_count', 'it_post_count', 'group_count',
#                'it_group_count']
labels1 = ['career', 'educ', 'it_descr',
            'it_group_prop', 'it_post_count', 'it_post_prop',
            'site', 'tight_post', 'tight_group']


def main(text):
    df = pd.DataFrame({'link': [text]})
    df['vk_id'] = df['link'].apply(lambda x: x.split('/')[-1])
    df, err = main_loop(df, feature='id', func=get_id, ident='vk_id')
    df['id'] = df['id'].astype('int')
    df, err = main_loop(df, feature='site', func=site)
    df, err = main_loop(df, feature='career', func=career)
    df, err = main_loop(df, feature='educ', func=educat)
    df, err = main_loop(df, feature='user_descr', func=get_user_descr)
    df, err = main_loop(df, feature='it_descr', func=it_descr)
    df['has_descr'] = df['user_descr'].apply(lambda x: 1 if x != '' else 0)
    df, err = main_loop(df, feature='group_count', func=group_count)
    df, err = main_loop(df, feature='it_group_count', func=it_group_count)
    df, err = main_loop(df, feature='post_count', func=post_count)
    df, err = main_loop(df, feature='it_post_count', func=it_post_count)

    df = df.loc[:, ~df.columns.str.match('Unnamed')]

    df['tight_post'] = df['post_count'].apply(lambda x: x if x <= 100 else 100)
    df['it_post_prop'] = df['it_post_count'] / (df['tight_post'] + 1)

    df['tight_group'] = df['group_count'].apply(lambda x: x if x <= 25 else 25)
    df['it_group_prop'] = df['it_group_count'] / (df['tight_group'] + 1)

    for i, path in enumerate(path_to_models1):
        with open(path, 'rb') as f:
            clf = pickle.load(f)
        X = df.loc[:, labels1].values
        y = clf.predict(X)
        df['model' + str(i)] = y

    # for i, path in enumerate(path_to_models2, len(path_to_models1)):
    #     with open(path, 'rb') as f:
    #         clf = pickle.load(f)
    #     X = df.loc[:, labels2].values
    #     y = clf.predict(X)
    #     df['model' + str(i)] = y

    return df

