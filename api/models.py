from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    protein_grams = models.FloatField(null=False, blank=False)
    carb_grams = models.FloatField(null=False, blank=False)
    fat_grams = models.FloatField(null=False, blank=False)


class NutritionEntry(models.Model):
    date = models.DateField(null=False, blank=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'NutritionEntries'
