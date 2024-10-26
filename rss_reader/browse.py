#

import sqlite3, time

import sql_functions as my

from importlib import reload
reload(my)

# Initialize sqlite
db_filename = "fetched.db"
con = sqlite3.connect(db_filename)

# Fetch ten most recent entries
entries = my.get_items(10)

# Print
