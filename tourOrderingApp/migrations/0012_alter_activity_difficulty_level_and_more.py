# Generated by Django 4.2.11 on 2024-04-18 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourOrderingApp', '0011_alter_activity_duration_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='difficulty_level',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='duration_hours',
            field=models.CharField(max_length=50),
        ),
    ]
