# Generated by Django 3.2.6 on 2021-08-27 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
