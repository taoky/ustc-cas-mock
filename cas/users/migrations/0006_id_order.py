# Generated by Django 3.2.6 on 2021-08-27 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='id',
            name='order',
            field=models.IntegerField(default=0, help_text='order 值越高，排列管理证件号 (glzjh) 时就越在前面。'),
        ),
    ]
