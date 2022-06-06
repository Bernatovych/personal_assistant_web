from django import template
from accounts.models import Profile
from ..models import Contact
from datetime import datetime, timedelta
register = template.Library()


def days_to_birthday(birthday):
    current_date = datetime.today().date()
    birthday = datetime.strptime(birthday, "%Y-%m-%d").replace(year=current_date.year).date()
    if birthday < current_date:
        birthday = birthday.replace(year=birthday.year + 1)
    days = (birthday - current_date).days
    return days


@register.inclusion_tag('holidays_period.html', takes_context=True)
def holidays_period(context):
    user = context['user']
    profile = Profile.objects.get(user=user)
    period = profile.period
    contacts = Contact.objects.filter(user=user)
    day_today = datetime.now()
    day_today_year = day_today.year
    end_period = day_today + timedelta(days=period)
    results = []
    for i in contacts:
        date = datetime.strptime(str(i.birthday), '%Y-%m-%d').replace(year=end_period.year)
        if day_today_year < end_period.year:
            if day_today <= date.replace(year=day_today_year) or date <= end_period:
                results.append((days_to_birthday(str(i.birthday)), i.__str__()))
        else:
            if day_today <= date.replace(year=day_today_year) <= end_period:
                results.append((days_to_birthday(str(i.birthday)), i.__str__()))
    results.sort()
    return {'results': results, 'period': period}
