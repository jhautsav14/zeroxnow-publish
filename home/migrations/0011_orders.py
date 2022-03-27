# Generated by Django 4.0.3 on 2022-03-27 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_delete_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('items_json', models.CharField(max_length=5000)),
                ('name', models.CharField(max_length=90)),
                ('email', models.CharField(max_length=111)),
                ('campus', models.CharField(max_length=111, null=True)),
                ('p_order_id', models.CharField(max_length=111, null=True)),
            ],
        ),
    ]
