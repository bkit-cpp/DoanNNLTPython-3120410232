# Generated by Django 5.0.3 on 2024-04-29 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_order_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
    ]
