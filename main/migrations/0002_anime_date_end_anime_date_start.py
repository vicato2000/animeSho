# Generated by Django 4.1.4 on 2022-12-28 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='date_end',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='date_start',
            field=models.DateField(null=True),
        ),
    ]