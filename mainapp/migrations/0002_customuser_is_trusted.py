# Generated by Django 5.1.2 on 2024-10-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_trusted',
            field=models.BooleanField(default=False),
        ),
    ]
