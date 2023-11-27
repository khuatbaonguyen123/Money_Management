from django.shortcuts import render,redirect
from .models import Account,Transfer
from django.contrib import messages
import datetime

# Create your views here.

def index(request) :
    return render(request, "transfer/index.html")

def add_transfer(request) :
    accounts = Account.objects.filter(userId=request.user)
    context = {
        'fromAccount' : accounts,
        'toAccount' : accounts,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'transfer/add_transfer.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'transfer/add_transfer.html', context)
        description = request.POST['description']
        date = request.POST['transferDate']
        fromAccountId = request.POST['fromAccount']
        toAccountId = request.POST['toAccount']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'transfer/add_transfer.html', context)
        
        fromAccount = Account.objects.get(pk=fromAccountId)
        toAccount = Account.objects.get(pk=toAccountId)
        Transfer.objects.create(from_account=fromAccount,amount=amount,to_account=toAccount,date=date,description=description)

        

        fromAccount.balance -= int(amount)
        toAccount.balance += int(amount)

        fromAccount.save()
        toAccount.save()

        messages.success(request, 'Transfer saved successfully')

        return redirect('transfer')
