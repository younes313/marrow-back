# Generated by Django 3.2.7 on 2021-09-03 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_movie_imdb_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='gross',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='imdb_rate_number',
        ),
    ]