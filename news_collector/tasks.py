import re
import requests
from bs4 import BeautifulSoup
from celery.schedules import crontab
from celery.task import periodic_task
from .models import ParseResult
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


SITE_LIST = (({'category': 'news', 'website': 'https://itc.ua/ua/novini/', 'element': 'h2', 'attribute': 'class',
                    'value': 'entry-title text-uppercase'}),
                ({'category': 'news', 'website':
                    'https://www.overclockers.ua/ua/news/', 'element': 'h2', 'attribute': '',
                    'value': ''}),
                ({'category': 'weather', 'website':
                    'https://www.meteoprog.ua/ua/', 'element': 'div', 'attribute': 'class',
                    'value': 'today-temperature'}),
                ({'category': 'weather', 'website': 'https://meteo.ua/34/kiev/', 'element': 'div', 'attribute': 'class',
                    'value': 'weather-detail__main-temp js-weather-detail-value'}),
                ({'category': 'weather', 'website':
                    'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2',
                    'element': 'p', 'attribute': 'class', 'value': 'today-temp'}),
                ({'category': 'football', 'website': 'https://football.ua/newsarc/',
                    'element': 'h4', 'attribute': '', 'value': ''}),
                ({'category': 'football', 'website': 'https://sport.ua/football',
                    'element': 'div', 'attribute': 'class', 'value': 'item-title'}),)


@periodic_task(run_every=(crontab(minute='*/2')), name="pars_task", ignore_result=True)
def pars_task():
    for site in SITE_LIST:
        website = site['website']
        page = requests.get(website)
        soup = BeautifulSoup(page.text, 'lxml')
        try:
            attribute = site['attribute']
        except IndexError:
            attribute = ''
        try:
            value = site['value']
        except IndexError:
            value = ''
        domain = urlparse(website).netloc
        if site['category'] == 'weather':
            if domain.startswith('www.'):
                domain = domain[4:]
            temp = soup.find(site['element'], attrs={attribute: value})
            try:
                temp = re.sub(r'[^0-9+-]+', r'', temp.text)
            except AttributeError:
                temp = 'no data'
            try:
                qs = ParseResult.objects.get(url=domain)
                qs.title = temp
                qs.save()
            except ParseResult.DoesNotExist:
                ParseResult.objects.create(url=domain, title=temp, category=site['category'])
        else:
            news = soup.findAll(site['element'], attrs={attribute: value})
            for i in news:
                try:
                    url = i.find('a').get('href')
                    valid_url = URLValidator()
                    try:
                        valid_url(url)
                        print(valid_url)
                    except ValidationError:
                        url = domain + url
                    try:
                        ParseResult.objects.get(title=i.text.strip())
                        pass
                    except ParseResult.DoesNotExist:
                        ParseResult.objects.create(url=url, title=i.text.strip(), category=site['category'])
                except AttributeError:
                    pass


