# Generated by Django 4.2.11 on 2024-06-07 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourOrderingApp', '0021_remove_booking_payment_remove_booking_tour_package_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelbooking',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='transportbooking',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
