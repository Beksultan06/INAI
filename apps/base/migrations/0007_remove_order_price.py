# Generated by Django 4.2.7 on 2024-11-23 00:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0006_order_price_order_quantity_order_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="price",
        ),
    ]
