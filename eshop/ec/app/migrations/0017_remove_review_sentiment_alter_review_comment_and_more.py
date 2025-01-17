# Generated by Django 5.1.1 on 2024-10-28 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_productimage_gif_url_alter_review_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='sentiment',
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app.product'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(),
        ),
    ]
