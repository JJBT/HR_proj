import vk
import vk.exceptions

import pandas as pd
import time

from Credentials import *

session = vk.Session(access_token=access_token)
api = vk.API(session, v=API_version)

corpus1 = pd.read_excel('data/corpus.xlsx')['words'].dropna().values
corpus2 = pd.read_excel('data/corpus.xlsx')['words_groups'].dropna().values


def main_loop(df, feature, func, start_idx=0):

    err_arr = []

    for idx, row in df.loc[start_idx:, :].iterrows():
        res = 0
        try:
            time.sleep(0.5)
            res = func(row['id'])
        except vk.exceptions.VkAPIError as e:
            print(e)
            print(idx, 'err')
            time.sleep(1)
            err_arr.append(idx)
        except BaseException as e:
            print(e)
            err_arr.append(idx)
            return df, err_arr

        print(idx, ' - ', res)
        df.loc[idx, feature] = res
    return df, err_arr


def get_id(user_id):
    resp = api.users.get(user_ids=user_id)
    return resp[0]['id']


def educat(user_id):
    resp = api.users.get(user_ids=user_id, fields='education')
    if 'university' in resp[0].keys():
        return 1
    return 0


def site(user_id):
    resp = api.users.get(user_ids=user_id, fields='site')
    if 'site' in resp[0].keys():
        if resp[0]['site'] != '':
            return 1
    return 0


def career(user_id):
    resp = api.users.get(user_ids=user_id, fields='career')
    if 'career' in resp[0].keys() and resp[0]['career']:
        return 1
    return 0


def get_user_descr(user_id):
    resp = api.users.get(user_ids=user_id, fields='about,interests,activities')
    arr = list([resp[0].get('about', ''), resp[0].get('interests', ''),  resp[0].get('activities', '')])
    arr = list(filter(lambda x: x != '', arr))
    return ' '.join(arr)


def it_descr(user_id):
    descr = get_user_descr(user_id)
    if it_text(descr, 1):
        return True
    return False


def group_count(user_id):
    resp = api.users.get(user_ids=user_id, fields='counters')
    print(resp)
    return resp[0]['counters'].get('pages', 0)


def groups(user_id):
    resp = api.users.getSubscriptions(user_id=user_id, fields='description,activity,status')
    return resp['groups']['items']


def it_group_count(user_id):
    items = groups(user_id)
    counter = 0

    for gr_id in items:
        if detect_it_group(gr_id):
            counter += 1
    return counter


def detect_it_group(group_id):
    time.sleep(0.4)
    resp = api.groups.getById(group_id=group_id, fields='description,activity,status')

    print(resp[0]['name'])

    activities = ['Программирование']

    if 'activity' in resp[0].keys():
        activity = resp[0]['activity']

        if activity in activities:
            return True

    arr = list([resp[0]['name'], resp[0].get('description', ''), resp[0].get('status', '')])
    arr = list(filter(lambda x: x != '', arr))
    text = ' '.join(arr)

    if it_text(text, 2):
        return True
    return False


def post_count(user_id):
    resp = api.wall.get(owner_id=user_id)
    return resp['count']


def it_post_count(user_id):
    resp = api.wall.get(owner_id=user_id, count=100)
    counter = 0

    for post in resp['items']:
        if detect_it_post(post):
            counter += 1
    return counter


def detect_it_post(post):
    attach = ''

    if 'attachments' in post.keys():
        if post['attachments'][0]['type'] == 'link':
            ur = post['attachments'][0]['link']['url']
            if ur:
                attach = ur
        elif post['attachments'][0]['type'] == 'video':
            attach = post['attachments'][0]['video']['title']

    text = ' '.join([post['text'], attach])
    text = clean_string(text, 'html')

    print(text)
    if it_text(text, 1):
        print('\t\tText True')
        return True

    if 'copy_history' in post.keys():
        source_id = str(post['copy_history'][0]['owner_id']).lstrip('-')

        if detect_it_group(source_id):
            print(True)
            return True

    return False


def it_text(s, n_corpus):
    s = s.lower()
    if n_corpus == 2:
        corpus = corpus2
    else:
        corpus = corpus1

    for item in corpus:
        if item in s:
            print('**' + item)
            return True
    return False


def clean_string(string, word):
    while string.find(word) != -1:
        string = string.replace(word, '')
    return string


path_to_df = 'Base.xlsx'
path_to_err_file = 'err.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(path_to_df)

    df, err = main_loop(df, 'it_group_count', it_group_count)
    df.to_excel(path_to_df)
    err_df = pd.Series(err)
    err_df.to_excel(path_to_err_file)
