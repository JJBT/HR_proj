from features import *


df = pd.read_excel(path_to_df)

df, err = main_loop(df, 'it_group_count', it_group_count)


df.to_excel(path_to_df)
err_df = pd.Series(err)
err_df.to_excel(path_to_err_file)
