# Generated by Django 4.2.1 on 2023-06-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_discount_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=2, verbose_name='Скидка для товара'),
        ),
    ]