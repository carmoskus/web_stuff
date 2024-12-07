import sqlite3, time, feedparser
from collections import namedtuple

def namedtuple_factory(cursor, row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)

# Tables
# source: details for where info is fetched from, an rss feed or something else
# fetch: a specific update of a specific feed
# item: a single rss entry or other bit retrieved and to be noted/tagged
# note: a tag or comment on an item

# source: type, url, status
# fetch: source_id, dbtime, stime, status
# item: fetch_id, url, title, author, content, status
# note: item_id, tag, content, status

# source type: rss, mastodon, 
# source status: 0 = disabled, 1 = enabled, 2 = troubled, 
# fetch status: 0 = disabled, 1 = success, 2 = failure, 3 = in progress,
# item status: 0 = disabled, 1 = normal, 2 = ignored, 3 = liked, 
# note status: 

def mk_fresh(con):
    cur = con.cursor()

    # source: type, url, status
    cur.execute('DROP TABLE IF EXISTS source;')
    cur.execute('''
    CREATE TABLE source (
        source_id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        url TEXT NOT NULL,
        dbtime INTEGER DEFAULT (unixepoch()) NOT NULL,
        status INTEGER DEFAULT (1) NOT NULL
    );
    ''')

    # fetch: source_id, dbtime, stime, status
    cur.execute('DROP TABLE IF EXISTS fetch;')
    cur.execute('''
    CREATE TABLE fetch (
        fetch_id INTEGER PRIMARY KEY,
        source_id INTEGER NOT NULL,
        stime INTEGER,
        dbtime INTEGER DEFAULT (unixepoch()) NOT NULL,
        status INTEGER DEFAULT (2) NOT NULL,
        FOREIGN KEY (source_id) REFERENCES source (source_id)
    );
    ''')

    # item: fetch_id, url, title, author, content, status
    cur.execute('DROP TABLE IF EXISTS item;')
    cur.execute('''
    CREATE TABLE item (
        item_id INTEGER PRIMARY KEY,
        fetch_id INTEGER NOT NULL,
        url TEXT NOT NULL,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        stime INTEGER,
        dbtime INTEGER DEFAULT (unixepoch()) NOT NULL,
        status INTEGER DEFAULT (1) NOT NULL,
        FOREIGN KEY (fetch_id) REFERENCES fetch (fetch_id)
    );
    ''')

    # note: item_id, tag, content, status
    cur.execute('DROP TABLE IF EXISTS note;')
    cur.execute('''
    CREATE TABLE note (
        note_id INTEGER PRIMARY KEY,
        item_id INTEGER NOT NULL,
        tag TEXT NOT NULL,
        content TEXT NOT NULL,
        status INTEGER DEFAULT (1) NOT NULL,
        FOREIGN KEY (item_id) REFERENCES item (item_id)
    );
    ''')

def add_source(con, source_type: str, url: str):
    cur = con.cursor()
    cur.execute('INSERT INTO source (type, url) VALUES (?, ?)', (source_type, url))
    con.commit()
    res = cur.execute('SELECT source_id FROM source WHERE rowid = last_insert_rowid()').fetchone()
    return res[0]
def add_fetch(con, source_id: int, status: int, stime: int | None):
    cur = con.cursor()
    cur.execute('INSERT INTO fetch (source_id, status, stime) VALUES (?, ?, ?)', (source_id, status, stime, ))
    con.commit()
    res = cur.execute('SELECT fetch_id FROM fetch WHERE rowid = last_insert_rowid()').fetchone()
    return res[0]
def add_item(con, fetch_id: int, url: str, title: str, author: str, content: str):
    cur = con.cursor()
    cur.execute('INSERT INTO item (fetch_id, url, title, author, content) VALUES (?, ?, ?, ?, ?)', 
                (fetch_id, url, title, author, content))
    con.commit()
    res = cur.execute('SELECT item_id FROM item WHERE rowid = last_insert_rowid()').fetchone()
    return res[0]
def add_note(con, item_id: int, tag: str, content: str):
    cur = con.cursor()
    cur.execute('INSERT INTO note (item_id, tag, content) VALUES (?, ?, ?)', 
                (item_id, tag, content))
    con.commit()
    res = cur.execute('SELECT note_id FROM note WHERE rowid = last_insert_rowid()').fetchone()
    return res[0]


def get_rss_source_ids(con):
    cur = con.cursor()
    return [x[0] for x in cur.execute('SELECT source_id FROM source WHERE type = "rss"').fetchall()]
def get_rss_sources(con):
    cur = con.cursor()
    return cur.execute('SELECT source_id, url FROM source WHERE type = "rss"').fetchall()
def get_source_url(con, source_id: int):
    cur = con.cursor()
    return cur.execute('SELECT url FROM source WHERE source_id = ?', (source_id, )).fetchone()[0]

def get_items(con, n:int = 10):
    cur = con.cursor()
    cur.row_factory = namedtuple_factory
    # ORDER BY DESC dbtime 
    return cur.execute('''
        SELECT i.item_id, i.fetch_id, f.source_id, i.url, i.title, i.author, i.content, i.status 
        FROM item i INNER JOIN fetch f ON f.fetch_id = i.fetch_id 
        WHERE i.status = 1
        ORDER BY i.item_id DESC
        LIMIT ?
    ''', (n, )).fetchall()

def get_items_distinct(con, n:int = 10):
    cur = con.cursor()
    cur.row_factory = namedtuple_factory
    # ORDER BY DESC dbtime 
    return cur.execute('''
        SELECT i.item_id, i.fetch_id, f.source_id, i.url, i.title, i.author, i.content, i.status 
        FROM item i INNER JOIN fetch f ON f.fetch_id = i.fetch_id 
        WHERE i.status = 1
        GROUP BY f.source_id HAVING i.item_id = MAX(i.item_id)
        ORDER BY i.item_id DESC
        LIMIT ?
    ''', (n, )).fetchall()

def run_fetch(con, source_id: int):
    url = get_source_url(con, source_id)
    print(url)
    feed = feedparser.parse(url)
    if feed.bozo:
        print(f"BOZO: {url}")
        return add_fetch(con, source_id, 2, None)
    
    # Get source last updated time
    stime = None
    try:
        stime = int(time.mktime(feed.feed.updated_parsed))
    except AttributeError:
        pass

    # Add fetch entry
    fetch_id = add_fetch(con, source_id, 1, stime)

    # Add items
    for entry in feed.entries[::-1]:
        content = entry.summary
        if len(entry.get("content", [])) > 0:
            content = "\n".join(x.value for x in entry.content)
        add_item(con, fetch_id, entry.id, entry.title, entry.get('author', ''), content)
    
    return fetch_id
