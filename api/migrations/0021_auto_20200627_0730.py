# Generated by Django 3.0.7 on 2020-06-27 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20200618_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='plan',
            field=models.CharField(choices=[('maintenance', 'Weight Maintenance'), ('gradual_loss', 'Gradual Weight Loss'), ('rapid_loss', 'Rapid Weight Loss'), ('turbo_loss', 'Turbo Weight Loss')], default='gradual_loss', max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ideal_body_weight',
            field=models.IntegerField(default=150),
        ),
    ]
