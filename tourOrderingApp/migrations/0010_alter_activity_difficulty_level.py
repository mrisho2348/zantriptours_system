# Generated by Django 4.2.11 on 2024-04-18 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourOrderingApp', '0009_alter_transportation_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='difficulty_level',
            field=models.CharField(max_length=20),
        ),
    ]
