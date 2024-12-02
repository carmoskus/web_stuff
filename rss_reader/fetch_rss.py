#

import feedparser, time, sqlite3

import sql_functions as my

# from importlib import reload
# reload(my)

feed_list = [
    "https://pluralistic.net/feed/",
    "https://www.lawdork.com/feed",
    # "https://talkingpointsmemo.com/feed",
    "https://talkingpointsmemo.com/edblog/feed",
    "https://digbysblog.net/feed/",
    "https://www.propublica.org/feeds/propublica/main",
    "https://alamedapost.com/feed/",
    "https://www.readtpa.com/feed"
]

parsed_list = [feedparser.parse(x) for x in feed_list]

[x.keys() for x in parsed_list]
[x.feed.keys() for x in parsed_list]

[x.bozo for x in parsed_list]

# fetch utime
[int(time.mktime(x.feed.updated_parsed)) for x in parsed_list]

print("\n\n".join(f"{i}\t" + str(x.entries[0].keys()) for i,x in enumerate(parsed_list)))
print("\n\n".join(f"{i}\t" + str(x.entries[0].get('content')) for i,x in enumerate(parsed_list)))
print("\n\n".join(f"{i}\t" + str(x.entries[0].summary_detail.value) for i,x in enumerate(parsed_list)))

parsed_list[4].entries[0].keys()

parsed_list[0].entries[0].content[0].value[:999]
parsed_list[0].entries[0].summary_detail.value[:999]

parsed_list[1].entries[0].content[0].value[:999]
parsed_list[1].entries[0].summary_detail.value[:999]

parsed_list[2].entries[0].content[0].value[:999]
parsed_list[2].entries[0].summary_detail.value[:999]

parsed_list[3].entries[0].content[0].value[:999]
parsed_list[3].entries[0].summary_detail.value[:999]

# item url
[x.entries[0].id for x in parsed_list]


feed = feedparser.parse(feed_list[0])
feed2 = feedparser.parse("https://www.readtpa.com/feed")

print(feed)
len(feed)
feed.keys()

for k, v in feed.items():
    print(k, type(v))

# bozo <class 'bool'>
# entries <class 'list'>
# feed <class 'feedparser.util.FeedParserDict'>
# headers <class 'dict'>
# etag <class 'str'>
# updated <class 'str'>
# updated_parsed <class 'time.struct_time'>
# href <class 'str'>
# status <class 'int'>
# encoding <class 'str'>
# version <class 'str'>
# namespaces <class 'dict'>

for k, v in feed.feed.items():
    print(k, type(v))

# title <class 'str'>
# title_detail <class 'feedparser.util.FeedParserDict'>
# links <class 'list'>
# link <class 'str'>
# subtitle <class 'str'>
# subtitle_detail <class 'feedparser.util.FeedParserDict'>
# updated <class 'str'>
# updated_parsed <class 'time.struct_time'>
# language <class 'str'>
# sy_updateperiod <class 'str'>
# sy_updatefrequency <class 'str'>
# generator_detail <class 'feedparser.util.FeedParserDict'>
# generator <class 'str'>
# image <class 'feedparser.util.FeedParserDict'>
# site <class 'str'>

for k, v in feed.entries[0].items():
    print(k, type(v))

# title <class 'str'>
# title_detail <class 'feedparser.util.FeedParserDict'>
# links <class 'list'>
# link <class 'str'>
# comments <class 'str'>
# authors <class 'list'>
# author <class 'str'>
# author_detail <class 'feedparser.util.FeedParserDict'>
# published <class 'str'>
# published_parsed <class 'time.struct_time'>
# tags <class 'list'>
# id <class 'str'>
# guidislink <class 'bool'>
# summary <class 'str'>
# summary_detail <class 'feedparser.util.FeedParserDict'>
# content <class 'list'>
# wfw_commentrss <class 'str'>
# slash_comments <class 'str'>
# post-id <class 'str'>

feed['etag']
feed['updated']
feed['href']
feed['status']
feed['encoding']
feed['version']

feed['headers']
feed['namespaces']

feed['entries']

entry = feed['entries'][0]
entry.keys()

for k, v in entry.items():
    print(k, type(v))

entry['title']
entry['title_detail']
entry['']

fetch_id = 1
for e in feed.entries:
    print(e.title)
    add_item(con, fetch_id, e.title, e.author, e.summary)
