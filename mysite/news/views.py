from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .models import News, Category
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.auth import login, logout

from news.tasks import send_mail_task


# Create your views here.


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 5

    # extra_context = {
    #     'title': "main",
    # }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Main page"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'
    # pk_url_kwarg = 'news_id'


class CreateNews(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registered succcessfully')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Register error")
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'news/register.html', context=context)


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }
    return render(request, 'news/login.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('home')


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        user_email = request.user.email
        print(user_email)
        if form.is_valid():
            mail = send_mail_task.delay(
                subject=form.cleaned_data['subject'],
                body=form.cleaned_data['body'],
                sender='olehk9999@gmail.com',
                list_of_receivers=['okutryk@gmail.com'],
            )
            # mail = send_mail(
            #     form.cleaned_data['subject'],
            #     form.cleaned_data['body'],
            #     'olehk9999@gmail.com',
            #     ['okutryk@gmail.com'],
            #     fail_silently=False
            # )
            if mail:
                messages.success(request, 'Email was sent successfully')
                return redirect('contact')
            else:
                messages.error(request, "Error: could not send your message")
        else:
            messages.error(request, "Validation error")

    else:
        form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'news/contact.html', context=context)

# def index(request):
#     news = News.objects.all().select_related('category')
#     paginator = Paginator(news, 4)
#     page_number = request.GET.get('page', 1)
#     page_news = paginator.get_page(page_number)
#
#     context = {
#         'page_obj': page_news,
#         "title": "list of news",
#     }
#     return render(request, "news/index.html", context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#
#     context = {
#         'news': news,
#         'category': category,
#     }
#     return render(request, template_name='news/category.html', context=context)


# def view_news(request, news_id: int):
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item
#     }
#     return render(request, 'news/view_news.html', context=context)
#
#
# def add_news(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'news/add_news.html', context)
