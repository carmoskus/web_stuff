#

import sqlite3

import sql_functions as my
from importlib import reload

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
print(new_sources)

reload(my)
for source_id in new_sources:
    my.run_fetch(con, source_id)
