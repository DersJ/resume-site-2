# Generated by Django 2.0.6 on 2018-06-12 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='slog',
            new_name='slug',
        ),
    ]
