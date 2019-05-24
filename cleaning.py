"""Deleting non-active accounts"""

import pandas as pd
import vk
import vk.exceptions
import time
import sys

from Credentials import *


session = vk.Session(access_token=access_token1)
api = vk.API(session, v=API_version)

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'mckinsey_test.xlsx'

df = pd.read_excel(filename)


err_arr = []

for idx, row in df.iterrows():
    print(idx)
    try:
        time.sleep(0.4)
        resp = api.users.get(user_ids=row['vk_id'])
        print(resp)
        if resp[0]['is_closed'] or ('deactived' in resp[0].keys()):
            err_arr.append(idx)
    except vk.exceptions.VkAPIError as e:
        print(e)
        if e.code == 113:
            print(idx, ' - ERR')
            err_arr.append(idx)
    except KeyError:
        err_arr.append(idx)

print(err_arr)

df.drop(err_arr, axis=0, inplace=True)
df.reset_index(inplace=True, drop=True)

filename_to_save = filename
df.to_excel(filename_to_save)
