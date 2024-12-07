#

import streamlit as st
import sqlite3, time

import sql_functions as my

# from importlib import reload
# reload(my)

# Initialize sqlite
db_filename = "fetched.db"
con = sqlite3.connect(db_filename)

def sel_reset():
  st.session_state.entries = []
  st.session_state.last_refresh_time = int(time.time())

def pull_recent(last_refresh_time):
    # Fetch ten most recent entries
    return tuple(my.get_items_distinct(con, 10))

# Print
st.set_page_config(layout = "wide")
st.title('FeedRSS')

if not 'last_refresh_time' in st.session_state:
  sel_reset()

st.session_state.last_refresh_time
st.button("Refresh", on_click=sel_reset, key="refresh")

st.session_state.entries = pull_recent(st.session_state.last_refresh_time)

seen_sources = set()

for entry in st.session_state.entries:
  if entry.source_id in seen_sources:
    continue
  seen_sources.add(entry.source_id)

  #  st.subheader(entry.title)
  with st.expander(entry.author + " - " + entry.title):
    st.text(entry.author)
    st.text(entry.url)
    if st.checkbox("View Source", key=f"vs{entry.item_id}"):
      st.code(entry.content, language=None)
    else:
      #  st.write(entry.content, unsafe_allow_html=True)
      st.html(entry.content)
