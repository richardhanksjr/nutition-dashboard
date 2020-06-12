# Generated by Django 3.0.7 on 2020-06-11 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NutritionEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protein_grams', models.FloatField()),
                ('carb_grams', models.FloatField()),
                ('fat_grams', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]