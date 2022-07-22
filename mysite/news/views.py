from django.http import HttpResponse
from django.shortcuts import render

from .models import News

# Create your views here.


def index(request):
    news = News.objects.all()
    res = "<h1>list</h1>"
    context = {
        'news': news,
        "title": "list of news"
    }
    return render(request, "news/index.html", context)

def test(request):
    return HttpResponse("<h1>Test page</h1>")
