# Generated by Django 5.0.6 on 2024-05-15 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dpauth", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="captchamodel",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
