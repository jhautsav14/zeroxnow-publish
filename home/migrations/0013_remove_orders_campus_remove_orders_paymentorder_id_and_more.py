# Generated by Django 4.0.3 on 2022-03-27 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_remove_orders_p_order_id_orders_paymentorder_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='campus',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='paymentorder_id',
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.CharField(max_length=111, primary_key=True, serialize=False),
        ),
    ]