from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views import View
from .models import NutritionEntry
from .forms import NutritionEntryForm
from django.utils.timezone import localdate
from django.contrib.auth.mixins import LoginRequiredMixin



class TestPath(View):
    def get(self, request):
        return HttpResponse("works")


class PERatio(LoginRequiredMixin, TemplateView):
    template_name = 'api/snippets/pe_ratio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todays_entries = NutritionEntry.objects.filter(date=localdate(),
                                                       user=self.request.user)
        total_protein = sum([entry.food.protein_grams for entry in todays_entries])
        total_energy = sum([entry.food.carb_grams + entry.food.fat_grams for entry in todays_entries])
        context['pe_ratio'] = total_protein / total_energy
        context['nutrition_entries'] = todays_entries
        return context


class NutritionEntryView(TemplateView):
    template_name = 'api/snippets/nutritionentry_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NutritionEntryForm
        return context




class NutritionEntryCreate(View):

    def post(self, request):
        form = NutritionEntryForm(request.POST)
        if form.is_valid():
            food = form.cleaned_data['food']
            num_servings = form.cleaned_data['num_servings']
            user = request.user
            NutritionEntry.objects.create(food=food, num_servings=num_servings,
                                          user=user)
        return HttpResponse("works")
