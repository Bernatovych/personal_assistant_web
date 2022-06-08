from django.urls import path
from . import views

app_name = "file_sorter"

urlpatterns = [
    path('', views.index, name='file_sorter'),
    path('upload', views.send_files, name="uploads")
]
