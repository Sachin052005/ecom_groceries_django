# Generated by Django 5.1.1 on 2024-10-28 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='sentiment',
            field=models.CharField(choices=[('Good', 'Good'), ('Neutral', 'Neutral'), ('Weak', 'Weak')], default='Neutral', max_length=10),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(),
        ),
    ]
