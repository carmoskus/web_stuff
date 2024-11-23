#

import requests, re
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup

# url = "https://mastodon.online/api/v1/accounts/111183843398906311" # account
# url = "https://mastodon.online/api/v1/accounts/111183843398906311/following" # following
# url = "https://mastodon.online/api/v1/accounts/111183843398906311/lists" # lists (needs login)
url = "https://mastodon.online/api/v1/accounts/111183843398906311/statuses?limit=10" # statuses

r = requests.get(url)
r

r.headers['Content-Type']

# print(r.text)
j = r.json()
j[0].keys()

for k in j[0].keys():
    print(k, type(j[0][k]))
# id <class 'str'>
# created_at <class 'str'>
# in_reply_to_id <class 'NoneType'>
# in_reply_to_account_id <class 'NoneType'>
# sensitive <class 'bool'>
# spoiler_text <class 'str'>
# visibility <class 'str'>
# language <class 'NoneType'>
# uri <class 'str'>
# url <class 'str'>
# replies_count <class 'int'>
# reblogs_count <class 'int'>
# favourites_count <class 'int'>
# edited_at <class 'NoneType'>
# content <class 'str'>
# reblog <class 'dict'>
# application <class 'NoneType'>
# account <class 'dict'>
# media_attachments <class 'list'>
# mentions <class 'list'>
# tags <class 'list'>
# emojis <class 'list'>
# card <class 'NoneType'>
# poll <class 'NoneType'>

j[0]['url']
j[0]['reblog']['url']

j[0]['created_at']
j[0]['reblog']['created_at']

j[0]['content']
j[0]['reblog']['content']

html_txt = j[19]['reblog']['content']
soup = BeautifulSoup(html_txt, 'html.parser')

soup

boost_list = [x for x in j if x['reblog'] is not None]
for x in boost_list:
    print(datetime.fromisoformat(x['created_at']).date())

start_today = datetime.now().date()
one_day_ago = start_today - timedelta(days=1)

[x for x in [datetime.fromisoformat(x['created_at']).date() for x in boost_list] 
 if x < start_today and x >= one_day_ago]

"""
Function to parse a BeautifulSoup object into needed info
"""
def parse_soup(soup):
    main_links = []
    for a in soup.find_all('a'):
        a_class = a.get('class')
        if a.get('href') is None or a_class is not None and ('mention' in a_class or 'hashtag' in a_class):
            # a.decompose()
            continue
        main_links.append(a)
    # Return based on how many links we parsed
    if len(main_links) == 1:
        a = main_links[0]
        print("---", a)
        # Work on shortening the displayed text for the url
        a_href = a['href']
        # a_text = a.get_text() # Is the text inside the link ever useful?
        # print('---', a_text)
        a.decompose()
        parsed_txt = " ".join(x.strip() for x in soup.get_text("\n").split("\n") if x.strip() != "")
        parsed_txt = parsed_txt.replace(" # ", " #")
        return 1, a_href, parsed_txt
    if len(main_links) > 1:
        # Might break tie if one of the links has an old date
        print('ERROR:', main_links)
        return len(main_links), 
    parsed_txt = " ".join(x.strip() for x in soup.get_text("\n").split("\n") if x.strip() != "")
    parsed_txt = parsed_txt.replace(" # ", " #")
    return 0, parsed_txt

""" 
Function to get boosts from one day before given date

"""
def get_daily_boosts(acc_id: str, my_date, max_id: str = ''):
    # TODO reverse the order of returned boosts, so it goes from past to future
    url = f"https://mastodon.online/api/v1/accounts/{acc_id}/statuses"
    if max_id is not None and max_id != '':
        url += "?max_id=" + max_id

    req = requests.get(url)
    if req.status_code != 200:
        return
    
    json = req.json()
    # TODO return to 1 day after testing
    one_day_before = my_date - timedelta(days=4)
    dates = [datetime.fromisoformat(x['created_at']).date() for x in json]
    used = [e for d, e in zip(dates, json) 
            if d < my_date and d >= one_day_before and e['reblog'] is not None]
    for entry in used:
        nm = entry['reblog']['account']['username']
        e_url = entry['reblog']['url']
        nm_txt = f"[{nm}]({e_url})"
        soup = BeautifulSoup(entry['reblog']['content'], 'html.parser')
        parsed = parse_soup(soup)
        if parsed[0] == 0:
            print(nm_txt)
            print('>', parsed[1])
        elif parsed[0] == 1:
            print(nm_txt, '-', "<"+parsed[1]+">")
            print('>', parsed[2])
        else:
            print(nm_txt, '???')
        print()

get_daily_boosts('111183843398906311', datetime.now().date() - timedelta(days=0))




soup_list = [BeautifulSoup(x['reblog']['content'], 'html.parser') for x in boost_list]
for i, soup in enumerate(soup_list):
    main_links = []
    for a in soup.find_all('a'):
        a_class = a.get('class')
        # TODO: add check that href actually exists
        if a_class is not None and ('mention' in a_class or 'hashtag' in a_class):
            # a.decompose()
            continue
        main_links.append(a)
    print(i, len(main_links))
    if len(main_links) == 1:
        a = main_links[0]
        a_href = a['href']
        a_text = a.get_text()
        a.decompose()
        parsed_txt = " ".join(x.strip() for x in soup.get_text("\n").split("\n") if x.strip() != "")
        parsed_txt = parsed_txt.replace(" # ", " #")
        print(a_href)
        print(parsed_txt)
    elif len(main_links) > 1:
        # Might break tie if one of the links has an old date
        print('ERROR:', main_links)
    else:
        parsed_txt = " ".join(x.strip() for x in soup.get_text("\n").split("\n") if x.strip() != "")
        parsed_txt = parsed_txt.replace(" # ", " #")
        print(parsed_txt)
    print()


j[0]['reblog']
j[0]['reblog']['reblog']

j[0]['reblog'].keys()
for k, v in j[0]['reblog'].items():
    print(k, type(v))
# id <class 'str'>
# created_at <class 'str'>
# in_reply_to_id <class 'NoneType'>
# in_reply_to_account_id <class 'NoneType'>
# sensitive <class 'bool'>
# spoiler_text <class 'str'>
# visibility <class 'str'>
# language <class 'str'>
# uri <class 'str'>
# url <class 'str'>
# replies_count <class 'int'>
# reblogs_count <class 'int'>
# favourites_count <class 'int'>
# edited_at <class 'NoneType'>
# content <class 'str'>
# reblog <class 'NoneType'>
# account <class 'dict'>
# media_attachments <class 'list'>
# mentions <class 'list'>
# tags <class 'list'>
# emojis <class 'list'>
# card <class 'dict'>
# poll <class 'NoneType'>


#
url = "https://mastodon.online/api/v1/accounts/111183843398906311/statuses" # statuses

r = requests.get(url)
r.headers['Content-Type']
r.headers['Link']

x = re.search(r'[&?]max_id=(\d+)', r.headers['Link'])
x.group(1)

url2 = "https://mastodon.online/api/v1/accounts/111183843398906311/statuses?max_id=" + x.group(1)

r2 = requests.get(url2)
r2.headers['Content-Type']
r2.headers['Link']
