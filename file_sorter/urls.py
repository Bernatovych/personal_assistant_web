from django.urls import path
from . import views


urlpatterns = [
    path('', views.FilesListView.as_view(), name="files_list"),
    path('file_add/', views.FilesAddFormView.as_view(), name="file_add"),
    path('images/', views.ImagesListView.as_view(), name="images"),
    path('documents/', views.DocumentsListView.as_view(), name="documents"),
    path('audio/', views.AudioListView.as_view(), name="audio"),
    path('video/', views.VideoListView.as_view(), name="video"),
    path('archives/', views.ArchivesListView.as_view(), name="archives"),
    path('other/', views.OtherListView.as_view(), name="other"),
    path('file_download/<int:pk>/', views.file_download, name="file_download"),
    path('file_delete/<int:pk>/', views.FileDeleteView.as_view(), name="file_delete"),
]