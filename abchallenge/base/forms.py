from django import forms

class AdvanceForm(forms.Form):
    acct = forms.CharField(max_length=15)
    amt = forms.FloatField()
    is_credit = forms.BooleanField(required=False)

