# Generated by Django 4.1.1 on 2022-09-27 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchs', '0012_alter_match_en_cours_date_alter_match_passé_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match_en_cours',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 22, 18, 56, 335873)),
        ),
    ]
