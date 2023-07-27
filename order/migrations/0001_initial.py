# Generated by Django 4.2.2 on 2023-07-27 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('adminapp', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=30, null=True)),
                ('order_total', models.FloatField()),
                ('status', models.CharField(choices=[('processed', 'processed'), ('pending', 'pending'), ('delivered', 'delivered'), ('New', 'New'), ('out for shipping', 'out for shipping'), ('canceled', 'canceled')], default='New', max_length=100)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_payment_details', to='payment.payment')),
                ('shipping_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.userprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('ordered', models.BooleanField(default=False)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='myorders', to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapp.product')),
                ('product_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.productcolor')),
                ('product_variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.productvariant')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CancelOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancel_reason', models.CharField(choices=[('Other reasons', 'Other reasons'), ('Wrong Size', 'Wrong Size')], max_length=100)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
