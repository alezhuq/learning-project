from django.urls import path
from .views import HomeNews, NewsByCategory, ViewNews, CreateNews




urlpatterns = [
   # path('', index, name="home"),
   # path('category/<int:category_id>/', get_category, name='category'),
   # path('news/add_news/', add_news, name='add_news'),

   path('', HomeNews.as_view(), name="home"),
   path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
   path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
   path('news/add_news/', CreateNews.as_view(), name='add_news'),
]
