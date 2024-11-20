#

import requests

# url = "https://mastodon.online/api/v1/accounts/111183843398906311" # account
# url = "https://mastodon.online/api/v1/accounts/111183843398906311/following" # following
# url = "https://mastodon.online/api/v1/accounts/111183843398906311/lists" # lists (needs login)
url = "https://mastodon.online/api/v1/accounts/111183843398906311/statuses?limit=3" # statuses

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

j[0]['reblog']
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

