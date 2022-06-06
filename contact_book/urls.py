from django.urls import path
from contact_book import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contact_add/', views.ContactAddView.as_view(), name='contact_add'),
    path('phone_add/<int:pk>/', views.PhoneAddView.as_view(), name='phone_add'),
    path('address_add/<int:pk>/', views.AddressAddView.as_view(), name='address_add'),
    path('email_add/<int:pk>/', views.EmailAddView.as_view(), name='email_add'),
    path('contact_update/<int:pk>/', views.ContactUpdateView.as_view(), name='contact_update'),
    path('contact_delete/<int:pk>/', views.ContactDeleteView.as_view(), name='contact_delete'),
    path('phone_update/<int:pk>/', views.PhoneUpdateView.as_view(), name='phone_update'),
    path('address_update/<int:pk>/', views.AddressUpdateView.as_view(), name='address_update'),
    path('email_update/<int:pk>/', views.EmailUpdateView.as_view(), name='email_update'),
    path('phone_delete/<int:pk>/', views.PhoneDeleteView.as_view(), name='phone_delete'),
    path('address_delete/<int:pk>/', views.AddressDeleteView.as_view(), name='address_delete'),
    path('email_delete/<int:pk>/', views.EmailDeleteView.as_view(), name='email_delete'),
]