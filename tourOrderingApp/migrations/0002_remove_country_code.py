# Generated by Django 4.2.11 on 2024-04-17 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourOrderingApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='code',
        ),
    ]