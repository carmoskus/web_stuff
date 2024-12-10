from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.utils.html import escape

from .models import Source

def index(request):
    all_sources = Source.objects.all()
    context = {"source_list": all_sources}
    return render(request, "rss_app/index.html", context)

def source(request, source_id):
    source = get_object_or_404(Source, pk=source_id)
    context = {"source": source}
    return render(request, "rss_app/source.html", context)
