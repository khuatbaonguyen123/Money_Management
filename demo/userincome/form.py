from django import forms
from accounts.models import Account
from .models import Income

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['account', 'amount', 'description']