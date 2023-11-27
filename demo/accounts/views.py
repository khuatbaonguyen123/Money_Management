from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def index(request):
    account = Account.objects.filter(userId=request.user)

    paginator = Paginator(account, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'account': account,
        'page_obj': page_obj,
    }
    return render(request, 'account/index.html',context)

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

def account_edit(request, id):
    accounts =Account.objects.get(pk=id)
    context = {
        'values': accounts,
        'account' : accounts,
    }
    if request.method == 'GET':
        return render(request, 'account/edit_account.html', context)
    if request.method == 'POST':
        balance = request.POST['balance']

        if not balance:
            messages.error(request, 'Balance is required')
            return render(request, 'account/edit_account.html', context)
        description = request.POST['description']
        account_name = request.POST['account_name']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'account/edit_account.html', context)
        messages.success(request, 'Record updated  successfully')

        return redirect('account')