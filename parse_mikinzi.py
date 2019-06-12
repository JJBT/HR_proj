import pandas as pd
import vk.exceptions
from Credentials import *


session = vk.Session(access_token=access_token1)
api = vk.API(session, v=API_version)

group = 'mckinseyrussia'
res = api.groups.getMembers(group_id=group, count=300, offset=5000)

df = pd.DataFrame({'id': res['items']})
df['vk_id'] = df['id'].apply(lambda x: 'id' + str(x))
df.to_excel('mckinsey_test.xlsx')
