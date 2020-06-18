from django.db import models
from django.contrib.auth import get_user_model

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    ideal_body_weight = models.IntegerField(null=False, blank=False)
    num_hours_eating_window = models.IntegerField(null=False, blank=False, default=8)
    include_meditation_in_app = models.BooleanField(default=False)


class Exercise(models.Model):
    EXERCISE_CHOICES = [
        ('high_intensity', 'High Intensity'),
        ('low_intensity', 'Low Intensity')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_type = models.CharField(choices=EXERCISE_CHOICES, max_length=20)
    date = models.DateField(auto_now_add=True)


class MeditationEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


