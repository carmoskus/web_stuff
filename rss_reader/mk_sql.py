#

import sqlite3

import sql_functions as my


# Initialize sqlite
db_filename = "fetched.db"
con = sqlite3.connect(db_filename)

# Setup
my.mk_fresh(con)

feed_list = [
    "https://pluralistic.net/feed/",
    "https://www.lawdork.com/feed",
    "https://talkingpointsmemo.com/edblog/feed",
    "https://digbysblog.net/feed/",
    "https://www.propublica.org/feeds/propublica/main",
]
new_sources = [my.add_source(con, 'rss', x) for x in feed_list]

