from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import escape
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

        obj = Item(source=source, 
                url=entry.id, 
                title=entry.title, 
                author=author, 
                content=content,
                pub_date=datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed)))
        obj.save()

    return HttpResponseRedirect(reverse("source", args=(source.id,)))

def add_source(request):
    newurl = request.POST["newurl"]

    source = Source(url=newurl)
    source.save()

    return HttpResponseRedirect(reverse("index"))
