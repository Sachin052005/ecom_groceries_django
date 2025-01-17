# Generated by Django 5.1.1 on 2024-10-28 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, 'Bad ★😡'), (2, 'Weak★★😟'), (3, 'Neutral★★★😐'), (4, 'Good ★★★★😊'), (5, 'Excellent ★★★★★😄')]),
        ),
    ]
