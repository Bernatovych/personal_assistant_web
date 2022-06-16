from django import template
from django.conf import settings
from news_collector.models import ParseResult
from datetime import datetime
from django.core.cache import cache
register = template.Library()
today = datetime.today()


@register.inclusion_tag('weather_list.html')
def weather():
    if 'weather_qs' in cache:
        return cache.get("weather_qs")
    else:
        weather_qs = ParseResult.objects.filter(category='weather')
        cache.set('weather_qs', {'weather_qs': weather_qs}, settings.REDIS_TIMEOUT)
        return {'weather_qs': weather_qs}


@register.inclusion_tag('news_list.html')
def news():
    if 'news_qs' in cache:
        return cache.get("news_qs")
    else:
        news_qs = ParseResult.objects.filter(category='news').filter(created__day=today.day).order_by('-created')[:5]
        cache.set('news_qs', {'news_qs': news_qs}, settings.REDIS_TIMEOUT)
        return {'news_qs': news_qs}


@register.inclusion_tag('football_list.html')
def football():
    if 'football_qs' in cache:
        return cache.get("football_qs")
    else:
        football_qs = ParseResult.objects.filter(category='football').filter(created__day=today.day).order_by('-created')[:5]
        cache.set('football_qs', {'football_qs': football_qs}, settings.REDIS_TIMEOUT)
        return {'football_qs': football_qs}

