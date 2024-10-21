#

import feedparser, time, sqlite3



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

[x.entries[0].keys() for x in parsed_list]
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
