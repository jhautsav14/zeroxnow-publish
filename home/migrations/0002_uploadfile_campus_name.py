# Generated by Django 4.0.3 on 2022-03-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='campus_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
