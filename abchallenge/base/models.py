from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

LOAN_LEN = 12

class Account(models.Model):
    acct_no = models.IntegerField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, db_column="user_id")
    principle = models.FloatField(null=False, blank=False) # should be balance


class Transaction(models.Model):
    trans_no = models.BigAutoField(primary_key=True, null=False, blank=False)
    in_acct = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="in_acct", db_column="in_acct_id")
    out_acct = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="out_acct", db_column="out_acct_id")
    amt = models.FloatField(null=False, blank=False)
    attempt_at = models.DateField(auto_now_add=True, null=False, blank=False)
    is_success = models.BooleanField(null=False, blank=False)
    # repayment_no = models.ForeignKey(Repayment, on_delete=models.CASCADE, null=True)


class Repayment(models.Model):
    def now_plus_days(day_amt):
        return datetime.now() + timedelta(days=day_amt)

    repayment_no = models.BigAutoField(primary_key=True, null=False, blank=False) # not needed
    acct = models.OneToOneField(Account, on_delete=models.CASCADE, db_column="acct_id") # acts as unique primary key
    total_amt = models.FloatField(null=False, blank=False)
    created_at = models.DateField(null=False, blank=False, auto_now_add=True)
    start_at = models.DateField(default=now_plus_days(7)) 
    end_at = models.DateField(default=now_plus_days(7*LOAN_LEN)) 
    num_defaults = models.IntegerField(null=False, blank=False, default=0)

    
