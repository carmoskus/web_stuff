
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


requests.head(
    feed_list[4],
    headers = {
        'If-Modified-Since': 'Thu, 23 Jan 2025 19:28:38 GMT'
    }
)

requests.head(
    feed_list[2],
    headers = {
        'If-Modified-Since': 'Thu, 23 Jan 2025 21:28:38 GMT'
    }
)

requests.head(
    feed_list[2],
    headers = {
        'If-None-Match': 'W/"6791739e-8c7"'
    }
)
