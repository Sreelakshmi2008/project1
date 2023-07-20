# Generated by Django 4.2.2 on 2023-07-14 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_alter_cancelorder_cancel_reason_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('out for shipping', 'out for shipping'), ('pending', 'pending'), ('processed', 'processed'), ('delivered', 'delivered'), ('New', 'New'), ('canceled', 'canceled')], default='New', max_length=100),
        ),
    ]
