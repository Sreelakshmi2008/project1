# Generated by Django 4.2.2 on 2023-07-11 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cart_cart_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='cart_total',
            new_name='coupon_total',
        ),
    ]
