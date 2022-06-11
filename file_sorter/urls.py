from django.urls import path
from . import views

urlpatterns = [
    path('', views.uploadfile, name='file_sorter'),
    # path('upload', views.send_files, name="uploads")
]
