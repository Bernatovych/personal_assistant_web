from django.urls import path
from contact_book import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
]