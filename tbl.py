import pandas as pd
import vk
import vk.exceptions
import time

client_id = '6933199'
acces_token = '38d6f7bf156227703caa449f71e234c94777cfaf1eb5734271a429c846fa64296f481d1c2b58a53560580'
API_version = '5.52'

"""Удаление недействительных аккаунтов"""

session = vk.Session(access_token=acces_token)
api = vk.API(session, v=API_version)

df = pd.read_excel('Base.xlsx')


err_arr = []

for idx, row in df.iterrows():
    print(idx)
    try:
        time.sleep(0.4)
        resp = api.users.get(user_ids=row['vk_id'])
    except vk.exceptions.VkAPIError as e:
        if e.code == 113:
            print(idx, ' - ERR')
            err_arr.append(idx)

df.drop(err_arr, axis=0, inplace=True)
df.reset_index(inplace=True, drop=True)
df.to_excel('Base.xlsx')
