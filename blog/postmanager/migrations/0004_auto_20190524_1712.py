# Generated by Django 2.2 on 2019-05-24 11:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('postmanager', '0003_auto_20190524_1707'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postimages',
            options={'verbose_name_plural': 'PostImages'},
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 24, 11, 42, 7, 627095, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 24, 11, 42, 7, 627126, tzinfo=utc)),
        ),
    ]
