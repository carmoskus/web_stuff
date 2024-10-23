#

import sqlite3

# Tables
# source: details for where info is fetched from, an rss feed or something else
# fetch: a specific update of a specific feed
# item: a single rss entry or other bit retrieved and to be noted/tagged
# note: a tag or comment on an item

# source: type, url, status
# fetch: source_id, dbtime, utime, status
# item: fetch_id, url, title, author, summary, status
# note: item_id, tag, content, status

# source type: rss, mastodon, 
# source status: 0 = disabled, 1 = enabled, 2 = troubled, 
# fetch status: 0 = disabled, 1 = success, 2 = failure, 3 = in progress,
# item status: 0 = disabled, 1 = normal, 2 = ignored, 3 = liked, 
# note status: 

def mk_fresh(con):
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS source')
    cur.execute('''
    CREATE TABLE source (
        source_id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        url TEXT NOT NULL,
        status INTEGER DEFAULT (1) NOT NULL,
    );
    ''')

    cur.execute('DROP TABLE IF EXISTS fetch')
    cur.execute('''
    CREATE TABLE fetch (
        fetch_id INTEGER PRIMARY KEY,
        source_id INTEGER NOT NULL,
        dbtime INTEGER DEFAULT (unixepoch()) NOT NULL,
        utime INTEGER,
        status INTEGER DEFAULT (2) NOT NULL,
        FOREIGN KEY (source_id) REFERENCES source (source_id)
    );
    ''')

    cur.execute('DROP TABLE IF EXISTS item')
    cur.execute('''
    CREATE TABLE item (
        item_id INTEGER PRIMARY KEY,
        fetch_id INTEGER NOT NULL,
        url TEXT NOT NULL,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        summary TEXT NOT NULL,
        status INTEGER DEFAULT (1) NOT NULL,
        FOREIGN KEY (fetch_id) REFERENCES fetch (fetch_id)
    );
    ''')

def add_source(con, source_type: str, url: str):
    cur = con.cursor()
    cur.execute('INSERT INTO source (type, url) VALUES (?, ?)', (source_type, url))
    con.commit()
    res = cur.execute('SELECT source_id FROM source WHERE rowid = last_insert_rowid()').fetchall()
    return res[0]
def get_rss_sources(con):
    cur = con.cursor()
    return cur.execute('SELECT source_id, url FROM source WHERE type = "rss"').fetchall()
def add_fetch(con, source_id: int):
    cur = con.cursor()
    cur.execute('INSERT INTO fetch (source_id) VALUES (?)', (source_id,))
    con.commit()
    res = cur.execute('SELECT fetch_id FROM fetch WHERE rowid = last_insert_rowid()').fetchall()
    return res[0]
def add_item(con, fetch_id: int, title: str, author: str, summary: str):
    cur = con.cursor()
    cur.execute('INSERT INTO item (fetch_id, title, author, summary) VALUES (?, ?, ?, ?)', 
                (fetch_id, title, author, summary))
    con.commit()
    res = cur.execute('SELECT item_id FROM item WHERE rowid = last_insert_rowid()').fetchall()
    return res[0]

feed_list = [
    "https://pluralistic.net/feed/",
    "https://www.lawdork.com/feed",
    # "https://talkingpointsmemo.com/feed",
    "https://talkingpointsmemo.com/edblog/feed",
    "https://digbysblog.net/feed/",
    "https://www.propublica.org/feeds/propublica/main",
]
new_sources = [add_source(con, 'rss', x) for x in feed_list]

# Main
db_filename = "fetched.db"

# Initialize sqlite
con = sqlite3.connect(db_filename)

# Setup
mk_fresh(con)
