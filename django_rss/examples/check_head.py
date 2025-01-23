
import requests

feed_list = [
    "https://pluralistic.net/feed/",
    "https://www.penny-arcade.com/feed",
    "https://xkcd.com/rss.xml",
    "https://www.lawdork.com/feed",
    "https://talkingpointsmemo.com/edblog/feed",
    "https://digbysblog.net/feed/",
    "https://www.propublica.org/feeds/propublica/main",
]

r1 = requests.head(feed_list[0])
r2 = requests.head(feed_list[1])

res = [requests.head(x) for x in feed_list]

for x in res:
    print(list(x.headers.keys()))

for x in res:
    print(x.headers.get("ETag"))

for x in res:
    print(x.headers.get("Last-Modified"))

