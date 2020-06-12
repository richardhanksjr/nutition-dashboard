from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    protein_grams = models.FloatField(null=False, blank=False)
    carb_grams = models.FloatField(null=False, blank=False)
    fat_grams = models.FloatField(null=False, blank=False)


class NutritionEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'NutritionEntries'


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # time_zone_preference =
