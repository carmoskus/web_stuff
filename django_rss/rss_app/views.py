from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.utils.html import escape

from .models import Source

def index(request):
    all_sources = Source.objects.all()
    context = {"source_list": all_sources}
    return render(request, "rss_app/index.html", context)
    # return HttpResponse("<p>Hello world. Next stop RSS:</p><code>" + escape(str(all_sources)) + "</code>")
