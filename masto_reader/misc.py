
import requests, re, collections
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def get_all_following(acct):
    url = "https://mastodon.online/api/v1/accounts/{}/following?limit=80".format(acct)
    full_list = []
    while True:
        res = requests.get(url)
        if res.status_code != 200:
            print("Something went wrong")
            return
        data = res.json()
        if len(data) == 0:
            break
        full_list += data
        if 'next' not in res.links:
            break
        url = res.links['next']['url']
    return full_list

all_following = get_all_following("111183843398906311")

def acct_to_server(txt):
    loc = txt.find('@')
    if loc == -1:
        return "mastodon.online"
    res = txt[loc+1:]
    return res

for x in all_following:
    if 'mstdn.social' in x['acct']:
        print(x['acct'], x['uri'], x['url'])

server_names = [acct_to_server(x['acct']) for x in all_following]
collections.Counter(server_names)

collections.Counter(x['bot'] for x in all_following)

tag_re = r'<.*?>'

for x in all_following:
    if '@a.gup.pe' not in x['acct']:
        print(x['acct'])
        print(re.sub(tag_re, '', x['note']))
        print()

