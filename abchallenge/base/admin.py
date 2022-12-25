from django.contrib import admin

# Register your models here.
from .models import Transaction, Account, Repayment


admin.site.register(Transaction)
admin.site.register(Account)
admin.site.register(Repayment)