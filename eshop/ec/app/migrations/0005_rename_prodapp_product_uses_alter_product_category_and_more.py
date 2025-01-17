# Generated by Django 5.1.1 on 2024-10-18 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='prodapp',
            new_name='uses',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('AR', 'Atta, Rice, Dal'), ('OG', 'Oil, Ghee'), ('DB', 'Dairy, Bakery'), ('PS', 'Pet Supplies'), ('SS', 'Spices, Salt, Sugar'), ('DF', 'Dry Fruits, Nuts, Seeds'), ('CN', 'Biscuits, Chips, Namkeens'), ('BE', 'Breakfast Essentials'), ('BS', 'Body, Skincare'), ('BG', 'Beauty, Grooming'), ('OC', 'Oral Care'), ('BA', 'Baby Care'), ('HW', 'Hygiene, Wellness'), ('LD', 'Laundry, Dishwash'), ('HC', 'Household, Cleaning'), ('HK', 'Home, Kitchen')], max_length=2),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('razorpay_order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razorpay_payment_status', models.CharField(blank=True, max_length=100, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orderplaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending')], default='Pending', max_length=50)),
                ('admin_notified', models.BooleanField(default=False)),
                ('canceled_date', models.DateTimeField(blank=True, null=True)),
                ('canceled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='canceled_orders', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.payment')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('gif_url', models.URLField(blank=True, max_length=500, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='app.product')),
            ],
        ),
    ]
