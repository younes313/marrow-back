# Generated by Django 3.2.7 on 2021-09-03 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]