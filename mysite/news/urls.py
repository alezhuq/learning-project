from django.urls import path
from .views import user_login, user_logout, register, HomeNews, NewsByCategory, ViewNews, CreateNews, contact

from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('', index, name="home"),
    # path('category/<int:category_id>/', get_category, name='category'),
    # path('news/add_news/', add_news, name='add_news'),
    #
    path('', cache_page(60)(HomeNews.as_view()), name="home"),
    path('', HomeNews.as_view(), name="home"),
    path('register/', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('contact/', contact, name="contact"),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add_news/', CreateNews.as_view(), name='add_news'),
]
