from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.timezone import localtime


# Model managers
class LowIntensityExerciseManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(exercise_type='low_intensity')


class HighIntensityExerciseManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(exercise_type='high_intensity')


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

User = get_user_model()


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    protein_grams = models.FloatField(null=False, blank=False)
    carb_grams = models.FloatField(null=False, blank=False)
    fat_grams = models.FloatField(null=False, blank=False)
    fiber_grams = models.FloatField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    class Meta:
        unique_together = [['user', 'name']]


class NutritionEntry(models.Model):
    today = localtime(timezone.now()).date()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_entered = models.DateTimeField(auto_now_add=True)
    protein_grams = models.FloatField(null=False, blank=False)
    carb_grams = models.FloatField(null=False, blank=False)
    fat_grams = models.FloatField(null=False, blank=False)
    fiber_grams = models.FloatField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    num_servings = models.FloatField(null=False, blank=False, default=1)

    def __str__(self):
        return f"{self.user.username}--{self.date}: {self.description}"

    class Meta:
        verbose_name_plural = 'NutritionEntries'

    @classmethod
    def total_protein_for_day(cls, user):
        nutrition_entries = NutritionEntry.objects.filter(user=user, date=cls.today)
        return sum([entry.protein_grams * entry.num_servings for entry in nutrition_entries])

    @classmethod
    def calculate_total_protein_color(cls, user):
        plan = user.user_profile.plan
        user_ideal_weight = user.user_profile.ideal_body_weight
        protein_multiplier = _plan_details[plan]['protein_multiplier']
        total_protein_for_day = cls.total_protein_for_day(user)
        if total_protein_for_day > (user_ideal_weight * protein_multiplier * 1.25):
            protein_color = "gold"
        elif total_protein_for_day > user_ideal_weight:
            protein_color = "green"
        elif total_protein_for_day > user_ideal_weight * protein_multiplier * .66:
            protein_color = "yellow"
        else:
            protein_color = "red"
        return protein_color

    @classmethod
    def calculate_num_meditations(cls, user, date=None):
        return MeditationEvent.objects.filter(date=cls.today, user=user).count()

    @classmethod
    def calculate_meditation_color(cls, user, **kwargs):
        num_meditations = cls.calculate_num_meditations(user, **kwargs)
        num_meditations_goal = _plan_details[user.user_profile.plan]['med_relax']
        if num_meditations >= num_meditations_goal:
            color = "green"
        elif num_meditations > 0:
            color = "yellow"
        else:
            color = "red"

        return color

    @classmethod
    def calculate_pe_ratio_color(cls, user):
        pe_ratio = cls.calculate_pe_ratio(user)
        user_plan = user.user_profile.plan
        pe_goal = _plan_details[user_plan]['pe_ratio']

        if pe_ratio > pe_goal * 1.25:
            color = "gold"
        elif pe_ratio >= pe_goal:
            color = "green"
        elif pe_ratio >= pe_goal * .75:
            color = "yellow"
        else:
            color = "red"

        return color

    @classmethod
    def calculate_total_energy(cls, user):
        nutrition_entries = NutritionEntry.objects.filter(user=user, date=cls.today)
        return sum([((entry.carb_grams - entry.fiber_grams) + entry.fat_grams) * entry.num_servings for entry in
                    nutrition_entries])

    @classmethod
    def calculate_pe_ratio(cls, user):
        total_energy = cls.calculate_total_energy(user)
        total_protein = cls.total_protein_for_day(user)
        if total_energy:
            pe_ratio = total_protein / total_energy
        else:
            pe_ratio = total_protein

        return pe_ratio

    @classmethod
    def calculate_meditation_streak(cls, user):
        num_days_green = 0
        trackers = DailyTracking.objects.filter(user=user, date__lt=timezone.now().date()).order_by('-date')
        for tracker in trackers:
            print('meditation', tracker.meditation)
            if tracker.meditation == 'green' or tracker.meditation == 'gold':
                num_days_green += 1
            else:
                break
        return num_days_green

    @classmethod
    def calculate_exercise_streak(cls, user):
        num_days_green = 0
        trackers = DailyTracking.objects.filter(user=user, date__lt=timezone.now().date()).order_by('-date')
        for tracker in trackers:
            if tracker.exercise == 'green' or tracker.exercise == 'gold':
                num_days_green += 1
            else:
                break
        return num_days_green

    @classmethod
    def calculate_protein_streak(cls, user):
        num_days_green = 0
        trackers = DailyTracking.objects.filter(user=user, date__lt=timezone.now().date()).order_by('-date')
        for tracker in trackers:
            if tracker.protein_total == 'green' or tracker.protein_total == 'gold':
                num_days_green += 1
            else:
                break
        return num_days_green

    @classmethod
    def calculate_pe_streak(cls, user):
        num_days_green = 0
        trackers = DailyTracking.objects.filter(user=user, date__lt=timezone.now().date()).order_by('-date')
        for tracker in trackers:
            if tracker.pe_ratio == 'green' or tracker.pe_ratio == 'gold':
                num_days_green += 1
            else:
                break
        return num_days_green

class UserProfile(models.Model):
    PLAN_CHOICES = [
        ('super_charged', 'Super Charged'),
        ('aggressive', 'Aggressive Weight Loss'),
        ('moderate', 'Moderate Weight Loss'),
        ('slow', 'Slow Weight Loss'),
        ('maintenance', 'Weight Maintenance')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    ideal_body_weight = models.IntegerField(null=False, blank=False, default=150)
    include_meditation_in_app = models.BooleanField(default=False)
    plan = models.CharField(choices=PLAN_CHOICES, null=False, blank=False, default='slow', max_length=50)


class Exercise(models.Model):
    today = localtime(timezone.now()).date()

    EXERCISE_CHOICES = [
        ('high_intensity', 'High Intensity'),
        ('low_intensity', 'Low Intensity')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_type = models.CharField(choices=EXERCISE_CHOICES, max_length=20)
    date = models.DateField(auto_now_add=True)

    # Model managers
    objects = models.Manager()
    low_intensity = LowIntensityExerciseManger()
    high_intensity = HighIntensityExerciseManger()

    @classmethod
    def calculate_exercise_color(cls, user):
        hit_exercises = Exercise.objects.filter(user=user,
                                                exercise_type='high_intensity',
                                                date=cls.today)

        low_intensity_exercises = Exercise.objects.filter(user=user,
                                                          exercise_type='low_intensity',
                                                          date=cls.today)
        if hit_exercises and low_intensity_exercises:
            color = "gold"

        elif hit_exercises:
            color = "green"
        elif low_intensity_exercises:
            color = "yellow"
        else:
            color = "red"

        return color


class MeditationEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class DailyTracking(models.Model):
    today = localtime(timezone.now()).date()

    COLOR_CHOICES = [
        ('gold', 'gold'),
        ('green', 'green'),
        ('yellow', 'yellow'),
        ('red', 'red')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    exercise = models.CharField(choices=COLOR_CHOICES, default="red", max_length=20)
    pe_ratio = models.CharField(choices=COLOR_CHOICES, default="red", max_length=20)
    protein_total = models.CharField(choices=COLOR_CHOICES, default="red", max_length=20)
    meditation = models.CharField(choices=COLOR_CHOICES, default="red", max_length=20)
    eating_window = models.CharField(choices=COLOR_CHOICES, default="red", max_length=20)

    class Meta:
        unique_together = [['user', 'date']]

    @classmethod
    def update_user_tracking(cls, user):
        daily_tracking, _ = DailyTracking.objects.get_or_create(user=user, date=cls.today)
        daily_tracking.exercise = Exercise().calculate_exercise_color(user)
        daily_tracking.protein_total = NutritionEntry.calculate_total_protein_color(user)
        daily_tracking.pe_ratio = NutritionEntry.calculate_pe_ratio_color(user)
        daily_tracking.meditation = NutritionEntry.calculate_meditation_color(user)
        daily_tracking.save()

    def __str__(self):
        return f"P:E Ratio: {self.pe_ratio}, Total Protein: {self.protein_total}, Exercise: {self.exercise}, Meditations: {self.meditation}"


def create_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
