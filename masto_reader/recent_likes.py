#

import requests, re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# url = "https://mastodon.online/api/v1/accounts/111183843398906311" # account
# url = "https://mastodon.online/api/v1/accounts/111183843398906311/following" # following
# url = "https://mastodon.online/api/v1/accounts/111183843398906311/lists" # lists (needs login)
# url = "https://mastodon.online/api/v1/accounts/111183843398906311/statuses?limit=10" # statuses

# j = r.json()

# j[0].keys()
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

# j[0]['reblog'].keys()
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
        # print("---", a)
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
        # print('ERROR:', main_links)
        a_hrefs = [a['href'] for a in main_links]
        for a in main_links: 
            a.decompose()
        parsed_txt = " ".join(x.strip() for x in soup.get_text("\n").split("\n") if x.strip() != "")
        # TODO fix a similar issue with @ as we deal with here for #
        parsed_txt = parsed_txt.replace(" # ", " ")
        return len(main_links), a_hrefs, parsed_txt
    parsed_txt = " ".join(x.strip() for x in soup.get_text("\n").split("\n") if x.strip() != "")
    parsed_txt = parsed_txt.replace(" # ", " ")
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
    one_day_before = my_date - timedelta(days=1)
    dates = [datetime.fromisoformat(x['created_at']).date() for x in json]
    used = [e for d, e in zip(dates, json) 
            if d < my_date and d >= one_day_before and e['reblog'] is not None]
    results = []
    for entry in used:
        nm = entry['reblog']['account']['username']
        e_url = entry['reblog']['url']
        nm_txt = f"[{nm}]({e_url})"
        soup = BeautifulSoup(entry['reblog']['content'], 'html.parser')
        parsed = parse_soup(soup)
        results.append((nm_txt, ) + parsed)        
    # Check if the oldest entry we pulled is before one_day_before
    if dates[-1] < one_day_before:
        # Then we are finished
        return results
    
    # TODO compare to using the LINK header info
    new_max_id = json[-1]['id']
    return results + get_daily_boosts(acc_id, my_date, new_max_id)

def md_escape_text(parsed_string: str):
    return parsed_string.replace(
        '<', '\<').replace(
        '#', '\#').replace(
        '[', '\[').replace(
        '(', '\(').replace(
        '*', '\*')

# --- MAIN
n_days = 3
res_dates = [(datetime.now().date() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(n_days)]
res_list = [get_daily_boosts('111183843398906311', datetime.now().date() - timedelta(days=i))
            for i in range(n_days)]

for d, res in zip(res_dates, res_list):
    print(d, "---")
    fn = f"Generated/Mastodon-{d}.md"
    with open(fn, 'w') as out:
        for parsed in res[::-1]:
            if parsed[1] == 0:
                print(parsed[0], file=out)
                print('>', md_escape_text(parsed[2]), file=out)
            elif parsed[1] == 1:
                print(parsed[0], file=out)
                print('<'+parsed[2]+'>', file=out)
                print('>', md_escape_text(parsed[3]), file=out)
            else:
                print(parsed[0], file=out)
                for a_href in parsed[2]:
                    print('<'+a_href+'>', file=out)
                print('>', md_escape_text(parsed[3]), file=out)
            print(file=out)
