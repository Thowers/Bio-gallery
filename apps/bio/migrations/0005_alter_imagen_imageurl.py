# Generated by Django 5.1.7 on 2025-03-28 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio', '0004_merge_20250328_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imageurl',
            field=models.CharField(max_length=120),
        ),
    ]
