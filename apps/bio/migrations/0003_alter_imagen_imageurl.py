# Generated by Django 5.1.7 on 2025-03-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio', '0002_alter_imagen_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imageurl',
            field=models.URLField(max_length=500),
        ),
    ]
