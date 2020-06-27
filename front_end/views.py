from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localtime
from django.utils import timezone

# from api.forms import NutritionEntryForm
from api.models import NutritionEntry, Meal, Exercise, MeditationEvent as Meditation

GOLD = "background-color:black; border: 1px solid black;"
RED = "background-color:#CC0A37;"
YELLOW = "background-color:#FF8003;"
GREEN = "background-color:#03DAC5;"


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'front_end/index.html'
    RED_WIDTH = 25
    today = localtime(timezone.now()).date()

    def _pe_ratio(self, context, total_protein_for_day, total_energy):
        PE_GREEN_GOAL = 1.75
        if total_energy:
            pe_ratio = total_protein_for_day / total_energy
        else:
            pe_ratio = total_protein_for_day
        context['pe_text'] = f"{pe_ratio:.2f}/{PE_GREEN_GOAL}"
        if pe_ratio >= 2:
            context['pe_gold'] = True
            context['pe_width'] = 100

        elif pe_ratio >= PE_GREEN_GOAL:
            context['pe_green'] = True
            context['pe_width'] = 100
        elif pe_ratio >= 1.2:
            context['pe_yellow'] = True
            context['pe_width'] = 50
        else:
            context['pe_red'] = True
            context['pd_width'] = self.RED_WIDTH
        return context

    def _protein_context(self, context, total_protein_for_day):
        user_ideal_weight = self.request.user.user_profile.ideal_body_weight
        if total_protein_for_day > (user_ideal_weight * 1.25):
            context['protein_gold'] = True
            context['total_protein_color'] = GOLD
            context['protein_width'] = 100
        elif total_protein_for_day > user_ideal_weight:
            context['total_protein_color'] = GREEN
            context['protein_green'] = True
            context['protein_width'] = 100

        elif total_protein_for_day > user_ideal_weight * .66:
            context['protein_yellow'] = True
            context['protein_width'] = 50
            context['total_protein_color'] = YELLOW
        else:
            context['protein_red'] = True
            context['protein_width'] = self.RED_WIDTH
            context['total_protein_color'] = RED

        context['protein_text'] = f"{total_protein_for_day:.2f}/{user_ideal_weight}"
        return context

    def _exercise_context(self, context):

        context['exercise_choices'] = Exercise.get_exercise_type_display(Exercise)
        hit_exercises = Exercise.objects.filter(user=self.request.user,
                                                exercise_type='high_intensity',
                                                date=self.today)
        low_intensity_exercises = Exercise.objects.filter(user=self.request.user,
                                                          exercise_type='low_intensity',
                                                          date=self.today)
        if hit_exercises and low_intensity_exercises:
            context['exercise_gold'] = True
            context['exercise_width'] = 100
            context['exercise_text'] = "HIT + Activity!"
        elif hit_exercises:
            context['exercise_green'] = True
            context['exercise_width'] = 100
            context['exercise_text'] = "HIT"

        elif low_intensity_exercises:
            context['exercise_yellow'] = True
            context['exercise_width'] = 50
            context['exercise_text'] = "Activity"
        else:
            context['exercise_red'] = True
            context['exercise_width'] = self.RED_WIDTH

        context['hit_exercises'] = hit_exercises
        context['low_intensity'] = low_intensity_exercises
        return context

    def _eating_context(self, context):
        user = self.request.user
        meals = NutritionEntry.objects.filter(date=self.today, user=user).order_by('time_entered')
        # Only calculate eating window if we have a first meal.   In template, check for 'fasting'
        if meals.first():
            context['fasting'] = False

            last_meal_time = meals.last().time_entered
            end_eating_time = meals.first().time_entered + timezone.timedelta(
                hours=user.user_profile.num_hours_eating_window)
            num_hours_yellow_window = 1
            if timezone.now() <= end_eating_time:
                context['fasting_width'] = 100
                context['fasting_green'] = True
                context['seconds_since_first_meal'] = (
                        timezone.timedelta(hours=user.user_profile.num_hours_eating_window)
                        - (timezone.now() - meals.first().time_entered)).total_seconds()
            elif end_eating_time <= timezone.now() < last_meal_time + timezone.timedelta(
                    hours=num_hours_yellow_window) and last_meal_time > end_eating_time:
                context['in_yellow'] = True
                context['fasting_width'] = 50
                context['fasting_yellow'] = True
                context['fasting_text'] = 'OUTSIDE OF EATING WINDOW'
            elif end_eating_time <= timezone.now():
                context['fasting_width'] = 100
                context['eating_done_green'] = True
                context['fasting_green'] = True
                context['fasting_text'] = 'OUTSIDE OF EATING WINDOW'
            else:
                context['fasting_width'] = self.RED_WIDTH
                context['in_red'] = True
                context['fasting_red'] = True
                context['fasting_text'] = 'OUTSIDE OF EATING WINDOW'

        else:
            context['fasting'] = True
            context['fasting_green'] = True
            context['fasting_width'] = 100
            context['fasting_text'] = 'FASTING'
        return context

    def _meditation_context(self, context):
        meditations = Meditation.objects.filter(date=self.today, user=self.request.user)
        num_meditations = meditations.count()
        if num_meditations > 1:
            context['meditation_green'] = True
            context['meditation_width'] = 100
        elif num_meditations == 1:
            context['meditation_yellow'] = True
            context['meditation_width'] = 50
        else:
            context['meditation_red'] = True
            context['meditation_width'] = self.RED_WIDTH
        context['meditation_text'] = f"{num_meditations}/2"
        context['meditations'] = meditations
        return context

    def get_context_data(self, **kwargs):
        user = self.request.user
        today = localtime(timezone.now()).date()
        context = super().get_context_data(**kwargs)
        nutrition_entries = NutritionEntry.objects.filter(user=user, date=today)
        context['meals'] = Meal.objects.filter(user=user)

        context['entries'] = nutrition_entries
        total_protein_for_day = sum([entry.protein_grams * entry.num_servings for entry in nutrition_entries])
        total_energy = sum([((entry.carb_grams - entry.fiber_grams) + entry.fat_grams) * entry.num_servings for entry in
                            nutrition_entries])
        context = self._pe_ratio(context, total_protein_for_day, total_energy)

        context = self._protein_context(context, total_protein_for_day)
        context = self._exercise_context(context)
        context = self._eating_context(context)
        context = self._meditation_context(context)

        return context
