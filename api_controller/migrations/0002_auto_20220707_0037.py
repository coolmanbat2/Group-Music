# Generated by Django 3.2.7 on 2022-07-07 00:37

import api_controller.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_controller', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.CharField(default=api_controller.models.generate_code, max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='votes_to_skip',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
