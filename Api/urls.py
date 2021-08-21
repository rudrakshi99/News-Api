from django.urls import path, include
from .views import  NewsAPI, NewsCreateAPI, NewsUpdateAPI

urlpatterns = [
    path('', NewsAPI.as_view(), name="news_api"),
    path('create', NewsCreateAPI.as_view(), name="news_create_api"),
    path('<int:id>', NewsUpdateAPI.as_view(), name="news_update_api"),
]