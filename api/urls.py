from django.urls import path, include
from .views import TestPath
from . import views


urlpatterns = [
    path('', TestPath.as_view(), name='test-path'),
    path('pe_ratio', views.PERatio.as_view(), name='pe_ratio'),
    path('nutrition_entry_load', views.NutritionEntryView.as_view(), name='nutrition-entry'),
    path('nutrition_entry_submit', views.NutritionEntryCreate.as_view(), name='new_nutrition_entry'),
    path('nutrition_api_search', views.NutritionAPISearch.as_view(), name='nutrition_api_search'),
    path('add_new_food', views.AddNewFood.as_view(), name='add_new_food'),
    path('add_existing_meal', views.AddExistingMeal.as_view(), name='add_existing_meal'),
    path('delete_entry', views.DeleteEntry.as_view(), name='delete_entry'),
    path('add_exercise', views.AddExercise.as_view(), name='add_exercise'),
    path('delete_exercise', views.DeleteExercise.as_view(), name='delete_exercise'),
    path('add_meditation', views.AddMeditation.as_view(), name='add_meditation'),
    path('delete_meditation', views.DeleteMeditation.as_view(), name='delete_meditation'),
    path('update_quantity', views.UpdateServingQuantity.as_view(), name='update_quantity'),

]