from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('pe_ratio', views.PERatio.as_view(), name='pe_ratio'),
]