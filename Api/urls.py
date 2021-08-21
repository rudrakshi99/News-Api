from django.urls import path, include
from .views import  NewsAPI, latest, NewsCreateAPI, NewsUpdateAPI

urlpatterns = [
    path('', NewsAPI.as_view(), name="question_api"),
    path('create', NewsCreateAPI.as_view(), name="question_create_api"),
    path('<int:id>', NewsUpdateAPI.as_view(), name="question_update_api"),
    path('latest', latest, name="latest"),
]