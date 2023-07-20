# Generated by Django 4.2.2 on 2023-07-11 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_remove_cart_cart_total_remove_cart_coupon_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='coupon_total',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_total',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon_total',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
