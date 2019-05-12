from features import *
import sys


filename = sys.argv[-1]


def postproccess(path_to_file):
    df = pd.read_excel(path_to_file)
    err_dict = {}

    print('Feature extracting...')
    
    df, err_dict['weighted_group_sum'] = main_loop(df, feature='weighted_group_sum', func=weighted_group_sum)

    df.to_excel(path_to_file)
    log_err(err_dict)


def log_err(err_dict):
    df = pd.DataFrame()
    for i in err_dict:
        if len(err_dict[i]) > 0:
            df = pd.concat([df, pd.DataFrame({i: err_dict[i]})], axis=1)
    df.to_excel('err.xlsx')


if __name__ == '__main__':
    postproccess(filename)

