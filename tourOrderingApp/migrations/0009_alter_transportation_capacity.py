# Generated by Django 4.2.11 on 2024-04-18 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourOrderingApp', '0008_alter_transportation_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportation',
            name='capacity',
            field=models.CharField(max_length=20),
        ),
    ]
