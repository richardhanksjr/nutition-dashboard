# Generated by Django 3.0.7 on 2020-06-15 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_auto_20200612_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('protein_grams', models.FloatField()),
                ('carb_grams', models.FloatField()),
                ('fat_grams', models.FloatField()),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='nutritionentry',
            name='food',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.AddField(
            model_name='nutritionentry',
            name='meal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Meal'),
            preserve_default=False,
        ),
    ]