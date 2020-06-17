from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localtime
from django.utils import timezone

# from api.forms import NutritionEntryForm
from api.models import NutritionEntry, Meal, Exercise
GOLD = "background-color:#EEE8AA; border: 1px solid black;"
RED = "background-color:red;"
YELLOW = "background-color:yellow;"
GREEN = "background-color:green;"


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'front_end/index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        today = localtime(timezone.now()).date()
        context = super().get_context_data(**kwargs)
        nutrition_entries = NutritionEntry.objects.filter(user=user, date=today)
        context['meals'] = Meal.objects.filter(user=user)
        if nutrition_entries.count() < 1:
            context['pe_ratio'] = 0
            context['pe_ratio_color'] = RED
            context['total_protein'] = 0
            context['total_protein_color'] = RED
            return context
        context['entries'] = nutrition_entries
        total_protein_for_day = sum([entry.protein_grams for entry in nutrition_entries])
        total_energy = sum([entry.carb_grams + entry.fat_grams for entry in nutrition_entries])
        pe_ratio = total_protein_for_day / total_energy
        context['pe_ratio'] = pe_ratio
        if pe_ratio >= 2.5:
            context['pe_ratio_color'] = GOLD
        elif pe_ratio >= 1.5:
            context['pe_ratio_color'] = GREEN
        elif pe_ratio >= 1.0:
            context['pe_ratio_color'] = YELLOW
        else:
            context['pe_ratio_color'] = RED
        context['total_protein'] = total_protein_for_day
        user_ideal_weight = user.user_profile.ideal_body_weight
        if total_protein_for_day > (user_ideal_weight * 1.25):
            context['total_protein_color'] = GOLD
        elif total_protein_for_day > user_ideal_weight:
            context['total_protein_color'] = GREEN
        elif total_protein_for_day > user_ideal_weight * .66:
            context['total_protein_color'] = YELLOW
        else:
            context['total_protein_color'] = RED

        context['exercise_choices'] = Exercise.get_exercise_type_display(Exercise)
        hit_exercises = Exercise.objects.filter(user=self.request.user,
                                                exercise_type='high_intensity',
                                                date=today)
        low_intesity_exercises = Exercise.objects.filter(user=self.request.user,
                                                         exercise_type='low_intensity',
                                                         date=today)
        if hit_exercises and low_intesity_exercises:
            context['exercise_color'] = GOLD
        elif hit_exercises:
            context['exercise_color'] = GREEN
        elif low_intesity_exercises:
            context['exercise_color'] = YELLOW
        else:
            context['exercise_color'] = RED

        first_meal_time = NutritionEntry.objects.filter(date=today, user=user).order_by('-time_entered')\
                        .first().time_entered
        eating_time = timezone.now() - first_meal_time
        if eating_time < timezone.timedelta(hours=user.user_profile.num_hours_eating_window):
            context['eating_time_color'] = GREEN
        else:
            context['eating_time_color'] = RED
        context['total_time_eating'] = str(timezone.now() - first_meal_time).split(".")[0]

        return context

