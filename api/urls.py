from django.urls import path, include
from .views import TestPath
from . import views


urlpatterns = [
    path('', TestPath.as_view(), name='test-path'),
    path('pe_ratio', views.PERatio.as_view(), name='pe_ratio'),

]