# Generated by Django 3.2.7 on 2022-07-07 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_controller', '0002_auto_20220707_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='votes_to_skip',
            field=models.IntegerField(default=1),
        ),
    ]
