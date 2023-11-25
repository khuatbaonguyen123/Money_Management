from django import forms
from .models import *
from accounts.models import Account

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['account', 'category', 'amount', 'date', 'description']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter accounts based on the logged-in user
        self.fields['account'].queryset = user.accounts.all()
    
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))