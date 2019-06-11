from features import *
import sys


# filename = sys.argv[-1]
filename = 'data/V4-9.xlsx'


def prepreproccess(path_to_file):
    df = pd.read_excel(path_to_file)
    err_dict = {}

    print('Id extracting...')
    df['vk_id'] = df['links'].apply(lambda x: x.split('/')[-1])
    df, err_dict['id'] = main_loop(df, feature='id', func=get_id, ident='vk_id')
    df['id'] = df['id'].astype('int')

    df.to_excel(path_to_file)
    log_err(err_dict)


def log_err(err_dict):
    df = pd.DataFrame()
    for i in err_dict:
        if len(err_dict[i]) > 0:
            df = pd.concat([df, pd.DataFrame({i: err_dict[i]})], axis=1)
    df.to_excel('err.xlsx')


if __name__ == '__main__':
    prepreproccess(filename)

