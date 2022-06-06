from django.urls import path
from note_book import views


urlpatterns = [
    path('', views.NotePageView.as_view(), name='note_book'),
    path('note_add/', views.NoteAddView.as_view(), name='note_add'),
    path('tag_add/<int:pk>/', views.TagAddView.as_view(), name='tag_add'),
    path('tag_update/<int:pk>/', views.TagUpdateView.as_view(), name='tag_update'),
    path('tag_delete/<int:pk>/', views.TagDeleteView.as_view(), name='tag_delete'),
    path('note_update/<int:pk>/', views.NoteUpdateView.as_view(), name='note_update'),
    path('note_delete/<int:pk>/', views.NoteDeleteView.as_view(), name='note_delete'),
]