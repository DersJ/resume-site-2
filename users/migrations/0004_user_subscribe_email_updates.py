# Generated by Django 3.2.13 on 2022-04-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220418_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribe_email_updates',
            field=models.BooleanField(default=True),
        ),
    ]
