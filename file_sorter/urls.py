from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='file_sorter'),
    path('upload', views.send_files, name="uploads")
]
