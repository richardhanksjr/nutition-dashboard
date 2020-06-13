from django.urls import path, include
from .views import TestPath
from . import views


urlpatterns = [
    path('', TestPath.as_view(), name='test-path'),
    path('pe_ratio', views.PERatio.as_view(), name='pe_ratio'),
    path('nutrition_entry_load', views.NutritionEntryView.as_view(), name='nutrition-entry'),
    path('nutrition_entry_submit', views.NutritionEntryCreate.as_view(), name='new_nutrition_entry'),

]