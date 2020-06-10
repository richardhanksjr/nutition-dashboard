from django.urls import path, include
from .views import TestPath


urlpatterns = [
    path('', TestPath.as_view(), name='test-path'),
]