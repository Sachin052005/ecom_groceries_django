# Generated by Django 5.1.1 on 2024-10-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_remove_customer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/'),
        ),
    ]
