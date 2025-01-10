from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
    items = Item.objects.filter(source=source).order_by("-pub_date")
    context = {"source": source, "item_list": items}
    return render(request, "rss_app/source.html", context)

def timeline(request):
    oldest_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=7)
    items = Item.objects.filter(status=0).filter(pub_date__gt=oldest_date).order_by('-pub_date')
    return render(request, "rss_app/timeline.html", {"item_list": items})

def fulltime(request):
    items = Item.objects.order_by('-pub_date')
    return render(request, "rss_app/timeline.html", {"item_list": items})

def fetch_source(request, source):
    feed = feedparser.parse(source.url)
    if feed.bozo:
        return HttpResponse(status=500)
    
    if feed.feed.get('title', "") != "":
        source.title = feed.feed.title
    if feed.feed.get('subtitle', "") != "":
        source.description = feed.feed.subtitle

    for entry in feed.entries:
        content = entry.summary
        if len(entry.get("content", [])) > 0:
            content = "\n".join(x.value for x in entry.content)

        author = entry.get('author', '')
        if author.startswith("by "):
            author = author[3:]

        if entry.published_parsed.tm_gmtoff is not None:
            tz = datetime.timezone(datetime.timedelta(seconds=entry.published_parsed.tm_gmtoff))
        else:
            tz = datetime.timezone(datetime.timedelta(seconds=0))
        my_date = datetime.datetime(*entry.published_parsed[:6], tzinfo=tz)

        Item.objects.get_or_create(
            source = source,
            guid = entry.id,
            defaults = {
                "source": source,
                "guid": entry.id, 
                "url": entry.link, 
                "title": entry.title, 
                "author": author, 
                "content": content,
                "pub_date": my_date,
            })

    source.last_fetched = datetime.datetime.now(datetime.UTC)
    source.save()
    return HttpResponseRedirect(reverse("source", args=(source.id,)))

def fetch_id(request, source_id):
    source = get_object_or_404(Source, pk=source_id)
    return fetch_source(request, source)

def fetch_all(request):
    sources = Source.objects.all()
    sub_responses = [
        fetch_source(request, source)
        for source in sources
        if datetime.datetime.now(datetime.UTC) - source.last_fetched > datetime.timedelta(hours=1)
    ]
    return HttpResponseRedirect(reverse("index"))

def add_source(request):
    newurl = request.POST["newurl"]

    source = Source(url=newurl)
    source.save()

    return HttpResponseRedirect(reverse("index"))

def mark_read(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.status = 1
    item.save()
    return JsonResponse({"status": "success", "item_id": item_id})
def mark_unread(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.status = 0
    item.save()
    return JsonResponse({"status": "success", "item_id": item_id})
