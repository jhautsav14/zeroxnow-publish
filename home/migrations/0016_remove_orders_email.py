# Generated by Django 4.0.3 on 2022-03-27 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_orders_campus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='email',
        ),
    ]