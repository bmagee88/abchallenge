# Generated by Django 4.1.4 on 2022-12-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="attempt_at",
            field=models.DateField(auto_now_add=True),
        ),
    ]