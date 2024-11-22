# Generated by Django 4.2.7 on 2024-11-22 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0002_product_order_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="product",
        ),
        migrations.CreateModel(
            name="OrderProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(verbose_name="Количество")),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="base.order",
                        verbose_name="Заказ",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="base.product",
                        verbose_name="Продукт",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Заказынные продукты",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.ManyToManyField(
                through="base.OrderProduct", to="base.product", verbose_name="Продукт"
            ),
        ),
    ]
