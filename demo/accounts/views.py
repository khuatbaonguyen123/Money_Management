from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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
    account =Account.objects.get(pk=id)
    context = {
        'values': account,
        'account' : account,
    }
    if request.method == 'GET':
        return render(request, 'account/edit_account.html', context)
    if request.method == 'POST':
        balance = request.POST['balance']

        if not balance:
            messages.error(request, 'Balance is required')
            return render(request, 'account/edit_account.html', context)
        
        description = request.POST['description']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'account/edit_account.html', context)
        

        account_name = request.POST['account_name']

        account.balance = balance
        account.description = description
        account.account_name = account_name
        account.save()

        messages.success(request, 'Account updated  successfully')
        return redirect('account')
    
def stats_view(request) :
    return render(request, 'account/statistic.html')

def account_amount(request) :
    accounts = Account.objects.filter(userId=request.user)
    
    finalrep = {}

    for x in accounts:
        finalrep[x.id] = x.balance

    return JsonResponse({'account_data': finalrep}, safe=False)
