#

import requests
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
j

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

html_txt = j[5]['reblog']['content']
soup = BeautifulSoup(html_txt, 'html.parser')

soup

soup_list = [BeautifulSoup(e['reblog']['content'], 'html.parser') for e in j if e['reblog'] is not None]

for i, soup in enumerate(soup_list):
    main_links = []
    for a in soup.find_all('a'):
        a_class = a.get('class')
        # TODO: add check that href actually exists
        if a_class is not None and ('mention' in a_class or 'hashtag' in a_class):
            a.decompose()
            continue
        main_links.append(a)
    print(i, len(main_links))
    if len(main_links) == 1:
        a = main_links[0]
        a_href = a['href']
        a_text = a.get_text()
        a.decompose()
        parsed_txt = " ".join(x for x in soup.get_text("\n").split("\n") if x != "")
        print(a_href)
        print(parsed_txt)
    elif len(main_links) > 1:
        print('ERROR:', main_links)
    else:
        parsed_txt = " ".join(x for x in soup.get_text("\n").split("\n") if x != "")
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

