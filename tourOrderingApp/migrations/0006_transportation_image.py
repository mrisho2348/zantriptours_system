# Generated by Django 4.2.11 on 2024-04-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourOrderingApp', '0005_tourcategory_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='transportation_images/'),
        ),
    ]
