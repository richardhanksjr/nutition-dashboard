from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path("<int:splash>", views.Index.as_view(), name='index-no-splash'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]