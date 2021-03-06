# Generated by Django 3.0.7 on 2020-06-11 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('protein_grams', models.FloatField()),
                ('carb_grams', models.FloatField()),
                ('fat_grams', models.FloatField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='nutritionentry',
            options={'verbose_name_plural': 'NutritionEntries'},
        ),
        migrations.RemoveField(
            model_name='nutritionentry',
            name='carb_grams',
        ),
        migrations.RemoveField(
            model_name='nutritionentry',
            name='fat_grams',
        ),
        migrations.RemoveField(
            model_name='nutritionentry',
            name='protein_grams',
        ),
        migrations.AlterField(
            model_name='nutritionentry',
            name='date',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='nutritionentry',
            name='food',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Food'),
            preserve_default=False,
        ),
    ]
