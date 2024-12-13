#
import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = "django_rss.settings"
django.setup()

#
import feedparser, datetime, time
from rss_app.models import Source, Item

Source.objects.all()
Item.objects.all().delete()

source_obj = Source.objects.get(url="https://xkcd.com/rss.xml")
source_url = source_obj.url

feed = feedparser.parse(source_url)
feed.bozo

for entry in feed.entries:
    content = entry.summary
    if len(entry.get("content", [])) > 0:
        content = "\n".join(x.value for x in entry.content)

    author = entry.get('author', '')
    if author.startswith("by "):
        author = author[:3]

    obj = Item(source=source_obj, 
               url=entry.id, 
               title=entry.title, 
               author=author, 
               content=content,
               pub_date=datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed)))
    print(repr(obj))
    obj.save()
