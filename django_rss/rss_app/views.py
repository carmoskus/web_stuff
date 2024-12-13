from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.utils.dateparse import parse_datetime
from django.urls import reverse

from .models import Source, Item

import feedparser, datetime, time

def index(request):
    all_sources = Source.objects.all()
    context = {"source_list": all_sources}
    return render(request, "rss_app/index.html", context)

def source(request, source_id):
    source = get_object_or_404(Source, pk=source_id)
    items = Item.objects.filter(source=source)
    context = {"source": source, "items": items}
    return render(request, "rss_app/source.html", context)

def fetch(request, source_id):
    source = get_object_or_404(Source, pk=source_id)

    # Delete old items
    Item.objects.filter(source=source).delete()

    feed = feedparser.parse(source.url)
    if feed.bozo:
        return HttpResponse(status=500)

    for entry in feed.entries:
        content = entry.summary
        if len(entry.get("content", [])) > 0:
            content = "\n".join(x.value for x in entry.content)

        author = entry.get('author', '')
        if author.startswith("by "):
            author = author[:3]

        if entry.published_parsed.tm_gmtoff is not None:
            tz = datetime.timezone(datetime.timedelta(seconds=entry.published_parsed.tm_gmtoff))
        else:
            tz = datetime.timezone(datetime.timedelta(seconds=0))
        my_date = datetime.datetime(*entry.published_parsed[:6], tzinfo=tz)

        # my_date = parse_datetime(entry.published)

        obj = Item(
            source = source,
            guid = entry.id, 
            url = entry.link, 
            title = entry.title, 
            author = author, 
            content = content,
            pub_date = my_date)
        obj.save()

    return HttpResponseRedirect(reverse("source", args=(source.id,)))

def add_source(request):
    newurl = request.POST["newurl"]

    source = Source(url=newurl)
    source.save()

    return HttpResponseRedirect(reverse("index"))
