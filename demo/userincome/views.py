from django.shortcuts import render, redirect
from .models import Source, Income
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
# Create your views here.
import datetime
from .models import Account


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    accounts = Account.objects.filter(userId=request.user)

    income = Income.objects.filter(account__in=accounts)  

    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'income': income,
        'page_obj': page_obj,
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    accounts = Account.objects.filter(userId=request.user)
    context = {
        'sources': sources,
        'accounts' : accounts,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        account_id = request.POST['account']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add_income.html', context)

        account_instance = Account.objects.get(pk=account_id)
        income = Income.objects.create(account=account_instance, amount=amount, date=date,
                                  source=source, description=description)
        
        # Update the balance of the associated account
        account_instance.balance += int(income.amount)
        account_instance.save()

        messages.success(request, 'Record saved successfully')

        return redirect('income')


@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income =Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)
        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('income')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'record removed')
    return redirect('income')

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    userAccount = Account.objects.filter(userId=request.user)
    
    finalrep = {}

    incomes = {}

    for account in userAccount:
        incomes = Income.objects.filter(
            account=account, date__gte=six_months_ago, date__lte=todays_date
        )

    def get_source(income):
        return income.source
    category_list = list(set(map(get_source, incomes)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount

    for x in incomes:
        for y in category_list:
            finalrep[y] = get_income_source_amount(y)

    return JsonResponse({'income_source_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'income/statistic.html')

