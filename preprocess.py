from features import *
import sys


filename = sys.argv[-1]


def preproccess(path_to_file):
    df = pd.read_excel(path_to_file)
    err_dict = {}

    print('Feature extracting...')
    df['vk_id'] = df['link'].apply(lambda x: x.split('/')[-1])
    df, err_dict['id'] = main_loop(df, feature='id', func=get_id, ident='vk_id')
    df['id'] = df['id'].astype('int')
    df, err_dict['site'] = main_loop(df, feature='site', func=site)
    df, err_dict['career'] = main_loop(df, feature='career', func=career)
    df, err_dict['educ'] = main_loop(df, feature='educ', func=educat)
    df, err_dict['user_descr'] = main_loop(df, feature='user_descr', func=get_user_descr)
    df, err_dict['it_descr'] = main_loop(df, feature='it_descr', func=it_descr)
    df['has_descr'] = df['user_descr'].apply(lambda x: 1 if x != '' else 0)
    df, err_dict['group_count'] = main_loop(df, feature='group_count', func=group_count)
    df, err_dict['it_group_count'] = main_loop(df, feature='it_group_count', func=it_group_count)
    df, err_dict['weighted_group_sum'] = main_loop(df, feature='weighted_group_sum', func=weighted_group_sum)
    df, err_dict['post_count'] = main_loop(df, feature='post_count', func=post_count)
    df, err_dict['it_post_count'] = main_loop(df, feature='it_post_count', func=it_post_count)

    df = df.loc[:, ~df.columns.str.match('Unnamed')]

    df['tight_post'] = df['post_count'].apply(lambda x: x if x <= 100 else 100)
    df['it_post_prop'] = df['it_post_count'] / (df['tight_post'] + 1)

    df['tight_group'] = df['group_count'].apply(lambda x: x if x <= 25 else 25)
    df['it_group_prop'] = df['it_group_count'] / (df['tight_group'] + 1)

    df.to_excel(path_to_file)
    log_err(err_dict)


def log_err(err_dict):
    df = pd.DataFrame()
    for i in err_dict:
        if len(err_dict[i]) > 0:
            df = pd.concat([df, pd.DataFrame({i: err_dict[i]})], axis=1)
    df.to_excel('err.xlsx')


if __name__ == '__main__':
    preproccess(filename)

