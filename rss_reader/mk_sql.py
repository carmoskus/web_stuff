#

import sqlite3

# Tables
# source: details for where info is fetched from, an rss feed or something else
# fetch: a specific update of a specific feed
# item: a single rss entry or other bit retrieved and to be noted/tagged

# source: type, url, 
# fetch: source_id, time, 
# item: fetch_id, title, author, summary

# source types: rss, mastodon, 

def mk_fresh(con):
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS source')
    cur.execute('''
    CREATE TABLE source (
        source_id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        url TEXT NOT NULL
    );
    ''')

    cur.execute('DROP TABLE IF EXISTS fetch')
    cur.execute('''
    CREATE TABLE fetch (
        fetch_id INTEGER PRIMARY KEY,
        source_id INTEGER NOT NULL,
        time INTEGER DEFAULT (unixepoch()) NOT NULL,
        FOREIGN KEY (source_id) REFERENCES source (source_id)
    );
    ''')

    cur.execute('DROP TABLE IF EXISTS item')
    cur.execute('''
    CREATE TABLE item (
        item_id INTEGER PRIMARY KEY,
        fetch_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        summary TEXT NOT NULL,
        FOREIGN KEY (fetch_id) REFERENCES fetch (fetch_id)
    );
    ''')

def add_source(con, source_type: str, url: str):
    cur = con.cursor()
    cur.execute('INSERT INTO source (type, url) VALUES (?, ?)', (source_type, url))
    con.commit()

# Main
db_filename = "fetched.db"

# Initialize sqlite
con = sqlite3.connect(db_filename)
cur = con.cursor()

# Setup
mk_fresh(con)
