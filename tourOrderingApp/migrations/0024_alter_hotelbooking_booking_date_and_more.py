# Generated by Django 4.2.11 on 2024-06-07 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourOrderingApp', '0023_alter_hotelbooking_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelbooking',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transportbooking',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]