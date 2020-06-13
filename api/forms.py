from django.forms import ModelForm
from .models import NutritionEntry


class NutritionEntryForm(ModelForm):

    class Meta:
        model = NutritionEntry
        fields = ['food', 'num_servings']
