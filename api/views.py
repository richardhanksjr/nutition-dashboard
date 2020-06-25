import requests
import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views import View
from django.urls import reverse
from .models import NutritionEntry
from .models import Meal, NutritionEntry, Exercise, MeditationEvent
# from .forms import NutritionEntryForm
from django.utils.timezone import localdate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils.timezone import now

# Mapping of unit ids and their respective unit abbreviations
units = {
    'urn:uuid:e0ad190a-d48b-443e-b637-e1cf05db2cdb': 'oz',
    'urn:uuid:3e8384f0-ea47-4fde-b7e1-a12747b28a30': 'lb',
    'urn:uuid:d3be684c-ebfa-4861-924f-8840600d1e84': 'g',
    'urn:uuid:0e5f4dd2-3353-477f-9773-0ed116c93e2e': 'Kg',
}

nutrients = {
    "urn:uuid:a4d01e46-5df2-4cb3-ad2c-6b438e79e5b9": "Calories",
    "urn:uuid:666ae7df-af65-4d55-8d5f-996e6cc384ca": "Protein",
    "urn:uuid:975a8d10-8650-4e0c-9a8f-7f4aaa6ae9e2": "Carbohydrates",
    "urn:uuid:7e53326a-e016-4560-ac5a-894c28e5085c": "Fiber",
    "urn:uuid:589294dc-3dcc-4b64-be06-c07e7f65c4bd": "Fat",
}

EDAMAM_API_KEY = settings.EDAMAM_API_KEY
EDAMAM_APPLICATION_ID = settings.EDAMAM_APPLICATION_ID
EDAMAM_URL = f"https://api.edamam.com/api/nutrition-details?app_id={EDAMAM_APPLICATION_ID}&app_key={EDAMAM_API_KEY}"


class TestPath(View):
    def get(self, request):
        return HttpResponse("works")


class PERatio(LoginRequiredMixin, TemplateView):
    template_name = 'api/snippets/pe_ratio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # todays_entries = NutritionEntry.objects.filter(date=localdate(),
        #                                                user=self.request.user)
        # total_protein = sum([entry.food.protein_grams for entry in todays_entries])
        # total_energy = sum([entry.food.carb_grams + entry.food.fat_grams for entry in todays_entries])
        # context['pe_ratio'] = total_protein / total_energy
        # context['nutrition_entries'] = todays_entries
        return context


class NutritionEntryView(TemplateView):
    template_name = 'api/snippets/nutritionentry_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = NutritionEntryForm
        context['nutrition_entries'] = NutritionEntry.objects.all()
        return context


class NutritionEntryCreate(View):

    def post(self, request):
        return HttpResponse("works")


class NutritionAPISearch(TemplateView):
    template_name = 'api/snippets/new_food_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search_term').split(",")

        response = requests.post(EDAMAM_URL, json={"ingr": search_term}).json()

        try:
            context['protein'] = response['totalNutrients']['PROCNT']
            context['carbs'] = response['totalNutrients']['CHOCDF']
            context['fat'] = response['totalNutrients']['FAT']
            context['fiber'] = response['totalNutrients']['FIBTG']
            context['ingredients'] = search_term
        except KeyError:
            context['api_error'] = "There was an error with this request. " \
                                   " Please alter the search term or do a manual entry"
        return context


class AddNewFood(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        protein = request.POST.get('protein')
        carbs = request.POST.get("carbs")
        fiber = request.POST.get("fiber")
        fat = request.POST.get("fat")
        meal_title = request.POST.get("meal_title")
        description = request.POST.get("description")
        # If we have a meal title, we want to save this for future use
        if meal_title:
            meal = Meal.objects.create(protein_grams=protein, carb_grams=carbs, fat_grams=fat, name=meal_title,
                                       description=description, user=user, fiber_grams=fiber)
        NutritionEntry.objects.create(user=user, protein_grams=protein, carb_grams=carbs, fat_grams=fat,
                                      fiber_grams=fiber,
                                      description=description)
        return HttpResponseRedirect(reverse('index'))


class AddExistingMeal(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        meal_name = request.POST.get("existing_meal_name")
        meal = Meal.objects.get(user=user, name=meal_name)
        entry, created = NutritionEntry.objects.get_or_create(user=user, protein_grams=meal.protein_grams,
                                                              carb_grams=meal.carb_grams,
                                                              fat_grams=meal.fat_grams, fiber_grams=meal.fiber_grams,
                                                              description=meal.description, date=now().date())
        # If the user has added another same entry instead of changing the servings amount, use the same entry and increment the count
        if not created:
            entry.num_servings += 1
            entry.save()
        return HttpResponseRedirect(reverse('index'))


class DeleteEntry(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get('id')
        entry = NutritionEntry.objects.get(id=id)
        # TODO fix this
        # if request.user is entry.user:
        entry.delete()
        return HttpResponseRedirect(reverse('index'))


class DeleteExercise(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get('id')
        entry = Exercise.objects.get(id=id)
        # TODO fix this
        # if request.user is entry.user:
        entry.delete()
        return HttpResponseRedirect(reverse('index'))


class AddExercise(LoginRequiredMixin, View):
    def post(self, request):
        exercises = {'1': 'high_intensity', '2': 'low_intensity'}
        exercise_number = request.POST.get("exercise_number")
        user = request.user
        Exercise.objects.create(user=user, exercise_type=exercises[exercise_number])
        return HttpResponseRedirect(reverse('index'))


class AddMeditation(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        MeditationEvent.objects.create(user=user)
        return HttpResponseRedirect(reverse('index'))


class DeleteMeditation(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get('id')
        meditation = MeditationEvent.objects.get(id=id)
        meditation.delete()
        return HttpResponseRedirect(reverse('index'))


class UpdateServingQuantity(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get('id')
        entry = NutritionEntry.objects.get(id=id)
        num_servings = request.POST.get('num_servings')
        entry.num_servings = num_servings
        entry.save()
        return HttpResponseRedirect(reverse('index'))

class AddOneServing(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get('id')
        entry = NutritionEntry.objects.get(id=id)
        entry.num_servings += 1
        entry.save()
        return HttpResponseRedirect(reverse('index'))