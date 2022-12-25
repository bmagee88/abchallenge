# Generated by Django 4.1.4 on 2022-12-24 15:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_alter_repayment_acct_alter_repayment_end_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repayment",
            name="acct",
            field=models.OneToOneField(
                db_column="acct_id",
                on_delete=django.db.models.deletion.CASCADE,
                to="base.account",
            ),
        ),
        migrations.AlterField(
            model_name="repayment",
            name="end_at",
            field=models.DateField(
                default=datetime.datetime(2023, 3, 18, 17, 20, 25, 917693)
            ),
        ),
        migrations.AlterField(
            model_name="repayment",
            name="start_at",
            field=models.DateField(
                default=datetime.datetime(2022, 12, 31, 17, 20, 25, 917693)
            ),
        ),
    ]
