# Generated by Django 2.2 on 2019-05-30 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postmanager', '0009_auto_20190529_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='postmanager.Tag'),
        ),
    ]
