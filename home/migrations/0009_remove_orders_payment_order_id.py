# Generated by Django 4.0.3 on 2022-03-27 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_rename_p_order_id_orders_payment_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='payment_order_id',
        ),
    ]