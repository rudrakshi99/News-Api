import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.http import HttpResponse
from .models import News

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "q": "nri",
    "hl": "en-In",
    "gl": "IN",
    "ceid": "IN",
    "tbm": "nws",
}

@shared_task
def task_news_update(request):
        # print("Task started")
        response = requests.get("https://www.google.com/search", headers=headers, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        for result in soup.select('.dbsr'):
            title = result.select_one('.nDgy9d').text
            link = result.a['href']
            source = result.select_one('.WF4CUc').text
            snippet = result.select_one('.Y3v8qd').text
            date_published = result.select_one('.WG9SHc span').text
            
            news = News(title=title, link=link, source=source, snippet=snippet, date_published=date_published)
            news.save()
            # print(f'{title}\n{link}\n{snippet}\n{date_published}\n{source}\n')
        
       