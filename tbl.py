import pandas as pd
import vk
import vk.exceptions
import time

from Credentials import *

"""Удаление недействительных аккаунтов"""

session = vk.Session(access_token=access_token)
api = vk.API(session, v=API_version)

df = pd.read_excel('Base.xlsx')


err_arr = []

for idx, row in df.iterrows():
    print(idx)
    try:
        time.sleep(1)
        resp = api.users.get(user_ids=row['vk_id'], fields='is')
        print(resp)
        if resp[0]['is_closed']:
            err_arr.append(idx)
    except vk.exceptions.VkAPIError as e:
        if e.code == 113:
            print(idx, ' - ERR')
            err_arr.append(idx)
    except KeyError:
        err_arr.append(idx)

print(err_arr)

df.drop(err_arr, axis=0, inplace=True)
df.reset_index(inplace=True, drop=True)
df.to_excel('Base.xlsx')
