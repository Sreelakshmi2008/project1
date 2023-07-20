# Generated by Django 4.2.2 on 2023-07-03 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_status_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('out for shipping', 'out for shipping'), ('processed', 'processed'), ('delivered', 'delivered'), ('canceled', 'canceled')], default='New', max_length=100),
        ),
    ]
