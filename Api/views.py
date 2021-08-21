from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView )
from .models import News
from .serializer import NewsSerializer
from .pagination import MyPageNumberPagination
from .task import task_news_update



class NewsAPI(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class    = MyPageNumberPagination


class NewsCreateAPI(CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
                  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)   # successfully CREATED
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # invalid data
    
    
class NewsUpdateAPI(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    
    lookup_field        = 'id'                                      # set the lookup field to id

    
    def retrieve(self, request, id=None):
        try:                                                        # try to get the question
            news = News.objects.get(id=id)
        except News.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)   # if not found, return 404
        
        serializer = NewsSerializer(news)                     # serialize the question

        return Response(serializer.data)                            # return the serialized question
    
    
    def put(self, request, id=None):
        try:                                                        # try to get the question
            news = News.objects.get(id=id)
        except News.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
        serializer = NewsSerializer(news, data=request.data)  # convert complex data by passing into serializer 
        if serializer.is_valid():                                   # check for validation of data
            serializer.save()
            return Response(serializer.data)                        # return updated the JSON response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # return error for invalid data


    def delete(self, request, id=None):
        try:
            news = News.objects.get(id=id)
        except News.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)  # return 404 if not found
        
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)         # return 204 if deleted



def latest(request):
    task_news_update.delay(1)
    