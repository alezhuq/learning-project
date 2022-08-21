from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewsForm
from .models import News, Category
from django.views.generic import ListView, DetailView, CreateView
from  django.urls import reverse_lazy


# Create your views here.


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         "title": "list of news",
#     }
#     return render(request, "news/index.html", context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)

    context = {
        'news': news,
        'category': category,
    }
    return render(request, template_name='news/category.html', context=context)


# def view_news(request, news_id: int):
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item
#     }
#     return render(request, 'news/view_news.html', context=context)
#
#
def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()

    context = {
        'form': form
    }
    return render(request, 'news/add_news.html', context)


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'

    # extra_context = {
    #     'title': "main",
    # }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Main page"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)



class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'
    # pk_url_kwarg = 'news_id'


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
