# Generated by Django 3.2.13 on 2022-06-29 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]