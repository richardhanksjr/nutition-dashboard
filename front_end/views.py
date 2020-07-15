from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localtime
from django.utils import timezone

# from api.forms import NutritionEntryForm
from api.models import (NutritionEntry, Meal, Exercise, MeditationEvent as Meditation,
                        DailyTracking)

GOLD = "background-color:black; border: 1px solid black;"
RED = "background-color:#CC0A37;"
YELLOW = "background-color:#FF8003;"
GREEN = "background-color:#03DAC5;"


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'front_end/index.html'
    RED_WIDTH = 100
    today = localtime(timezone.now()).date()

    _plan_details = {
        'super_charged': {
            "protein_multiplier": 1.4,
            "pe_ratio": 2.8,
            "med_relax": 3,
            "eating_window": 6
        },
        'aggressive': {
            'protein_multiplier': 1.3,
            'pe_ratio': 2.2,
            'med_relax': 3,
            'eating_window': 6
        },
        'moderate': {
            'protein_multiplier': 1.2,
            'pe_ratio': 1.7,
            'med_relax': 2,
            'eating_window': 8
        },
        'slow': {
            'protein_multiplier': 1.1,
            'pe_ratio': 1.3,
            'med_relax': 1,
            'eating_window': 8

        },
        'maintenance': {
            'protein_multiplier': 1.0,
            'pe_ratio': 1,
            'med_relax': 1,
            'eating_window': 10

        }
    }

    def _pe_ratio(self, context, total_protein_for_day, total_energy, user_plan):
        pe_green_goal = user_plan['pe_ratio']
        if total_energy:
            pe_ratio = total_protein_for_day / total_energy
        else:
            pe_ratio = total_protein_for_day
        context['pe_text'] = f"{pe_ratio:.2f}/{pe_green_goal}"
        if pe_ratio >= 2:
            context['pe_gold'] = True
            context['pe_width'] = 100

        elif pe_ratio >= pe_green_goal:
            context['pe_green'] = True
            context['pe_width'] = 100
        elif pe_ratio >= 1.2:
            context['pe_yellow'] = True
            context['pe_width'] = 100
        else:
            context['pe_red'] = True
            context['pe_width'] = 100
        return context

    def _protein_context(self, context, total_protein_for_day, user_plan):
        protein_multiplier = user_plan['protein_multiplier']
        user_ideal_weight = self.request.user.user_profile.ideal_body_weight
        protein_color = NutritionEntry.calculate_total_protein_color(self.request.user)
        if protein_color == 'gold':
            context['protein_gold'] = True
            context['total_protein_color'] = GOLD
            context['protein_width'] = 100
        elif protein_color == "green":
            context['total_protein_color'] = GREEN
            context['protein_green'] = True
            context['protein_width'] = 100

        elif protein_color == 'yellow':
            context['protein_yellow'] = True
            context['protein_width'] = 100
            context['total_protein_color'] = YELLOW
        else:
            context['protein_red'] = True
            context['protein_width'] = self.RED_WIDTH
            context['total_protein_color'] = RED

        context['protein_text'] = f"{total_protein_for_day:.2f}/{user_ideal_weight * protein_multiplier}"
        return context

    def _exercise_context(self, context):

        context['exercise_choices'] = Exercise.get_exercise_type_display(Exercise)

        hit_exercises = Exercise.high_intensity.filter(date=self.today,
                                                                  user=self.request.user)
        low_intensity_exercises = Exercise.low_intensity.filter(date=self.today,
                                                                user=self.request.user)
        exercise_color = Exercise.calculate_exercise_color(self.request.user)
        if exercise_color == 'gold':
            context['exercise_gold'] = True
            context['exercise_width'] = 100
            context['exercise_text'] = "HIT + Activity!"
        elif exercise_color == 'green':
            context['exercise_green'] = True
            context['exercise_width'] = 100
            context['exercise_text'] = "HIT"

        elif exercise_color == 'yellow':
            context['exercise_yellow'] = True
            context['exercise_width'] = 100
            context['exercise_text'] = "Activity"
        else:
            context['exercise_red'] = True
            context['exercise_width'] = self.RED_WIDTH

        context['hit_exercises'] = hit_exercises
        context['low_intensity'] = low_intensity_exercises
        return context

    def _eating_context(self, context, user_plan):
        num_hours_eating_window = user_plan['eating_window']
        user = self.request.user
        meals = NutritionEntry.objects.filter(date=self.today, user=user).order_by('time_entered')
        # Only calculate eating window if we have a first meal.   In template, check for 'fasting'
        if meals.first():
            context['fasting'] = False

            last_meal_time = meals.last().time_entered
            end_eating_time = meals.first().time_entered + timezone.timedelta(
                hours=num_hours_eating_window)
            num_hours_yellow_window = 1
            if timezone.now() <= end_eating_time:
                context['fasting_width'] = 100
                context['fasting_green'] = True
                context['seconds_since_first_meal'] = (
                        timezone.timedelta(hours=num_hours_eating_window)
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

    def _meditation_context(self, context, user_plan):
        num_meditations_goal = user_plan['med_relax']
        meditations = Meditation.objects.filter(date=self.today, user=self.request.user)
        num_meditations = meditations.count()
        if num_meditations >= num_meditations_goal:
            context['meditation_green'] = True
            context['meditation_width'] = 100
        elif num_meditations > 0:
            context['meditation_yellow'] = True
            context['meditation_width'] = 100
        else:
            context['meditation_red'] = True
            context['meditation_width'] = self.RED_WIDTH
        context['meditation_text'] = f"{num_meditations}/{num_meditations_goal}"
        context['meditations'] = meditations
        return context

    def get_context_data(self, **kwargs):
        user = self.request.user
        plan_details = self._plan_details[user.user_profile.plan]
        today = localtime(timezone.now()).date()
        context = super().get_context_data(**kwargs)
        nutrition_entries = NutritionEntry.objects.filter(user=user, date=today)
        # TODO Change this back to user
        # context['meals'] = Meal.objects.filter(user=user)
        context['meals'] = Meal.objects.all()

        context['entries'] = nutrition_entries
        # total_protein_for_day = sum([entry.protein_grams * entry.num_servings for entry in nutrition_entries])
        total_protein_for_day = NutritionEntry.total_protein_for_day(self.request.user)
        total_energy = sum([((entry.carb_grams - entry.fiber_grams) + entry.fat_grams) * entry.num_servings for entry in
                            nutrition_entries])
        context = self._pe_ratio(context, total_protein_for_day, total_energy, plan_details)

        context = self._protein_context(context, total_protein_for_day, plan_details)
        context = self._exercise_context(context)
        context = self._eating_context(context, plan_details)
        context = self._meditation_context(context, plan_details)

        # Update daily tracking
        DailyTracking.update_user_tracking(self.request.user)
        daily_tracking = DailyTracking.objects.get(user=self.request.user, date=self.today)
        print(daily_tracking)

        return context


