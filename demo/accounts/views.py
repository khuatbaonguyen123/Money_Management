from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account

# Create your views here.

def index(request):
    return render(request, 'account/index.html')

def add_account(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        balance = request.POST.get('balance')
        description = request.POST.get('description')

        new_account = Account.objects.create(
            account_name=name,
            balance=balance,
            description=description,
            userId=request.user
        )

        return redirect('account')

    return render(request, 'account/add_account.html')