# Generated by Django 5.1.2 on 2024-10-19 17:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_alter_account_last_api_call'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_api_call',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 19, 20, 54, 25, 155930), verbose_name='last api call'),
        ),
    ]
