# Generated by Django 5.1.2 on 2024-10-20 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-post_id'], 'verbose_name': 'Post'},
        ),
    ]
