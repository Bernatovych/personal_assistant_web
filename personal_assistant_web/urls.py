"""personal_assistant_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile_update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('accounts/signup/', views.UserSignUpView.as_view(), name='signup'),
    path('accounts/account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),
         name='password_reset_done'),
    path('accounts/reset/<str:uidb64>/<str:token>', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_complete'),
    path('', include('contact_book.urls')),
    path('note_book/', include('note_book.urls')),
    #path('file_sorter/', include('file_sorter.urls')),
    #path('news_collector/', include('news_collector.urls')),
]
