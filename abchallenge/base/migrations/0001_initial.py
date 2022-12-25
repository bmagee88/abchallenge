# Generated by Django 4.1.4 on 2022-12-22 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("acct_no", models.IntegerField(primary_key=True, serialize=False)),
                ("principle", models.FloatField()),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("trans_no", models.IntegerField(primary_key=True, serialize=False)),
                ("amt", models.FloatField()),
                ("attempt_at", models.DateField()),
                ("is_success", models.BooleanField()),
                (
                    "in_acct",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="in_acct",
                        to="base.account",
                    ),
                ),
                (
                    "out_acct",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="out_acct",
                        to="base.account",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Repayment",
            fields=[
                (
                    "repayment_no",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("total_amt", models.FloatField()),
                ("created_at", models.DateField(auto_now_add=True)),
                ("start_at", models.DateField(auto_now_add=True)),
                ("end_at", models.DateField(auto_now_add=True)),
                ("num_defaults", models.IntegerField(default=0)),
                (
                    "acct",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="base.account"
                    ),
                ),
            ],
        ),
    ]
