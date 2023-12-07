from django.shortcuts import render, redirect
from .models import Source, Income, Account
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json, datetime
from django.http import JsonResponse
# Create your views here.

@require_POST
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        user_accounts = Account.objects.filter(userId=request.user)
        income = Income.objects.filter(
            amount__istartswith=search_str, account__in=user_accounts) | Income.objects.filter(
            date__istartswith=search_str, account__in=user_accounts) | Income.objects.filter(
            description__icontains=search_str, account__in=user_accounts) | Income.objects.filter(
            source__icontains=search_str, account__in=user_accounts)
        data = income.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    accounts = Account.objects.filter(userId=request.user)

    income = Income.objects.filter(account__in=accounts).order_by('-date')

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
    accounts = Account.objects.filter(userId=request.user)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'accounts': accounts,
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
        account_id = request.POST['account']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)
        account_instance = Account.objects.get(pk=account_id)
        income.amount = amount
        income. date = date
        income.source = source
        income.description = description
        income.account = account_instance

        income.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('income')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'record removed')
    return redirect('income')

def income_source_summary(request):
    selected_month = request.GET.get('selected_month')

    if selected_month:
        # Parse the selected month and calculate the date range
        selected_month_date = datetime.datetime.strptime(selected_month, '%m/%Y').date()
        start_date = selected_month_date.replace(day=1)
        end_date = start_date + datetime.timedelta(days=92)
    else:
        # If no month is selected, default to the last 6 months
        todays_date = datetime.date.today()
        start_date = todays_date - datetime.timedelta(days=30*12)
        end_date = todays_date

    accounts = Account.objects.filter(userId=request.user)
    incomes = Income.objects.filter(account__in=accounts, date__gte=start_date, date__lte=end_date)

    finalrep = {}

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
    
    return JsonResponse({'income_source_data': finalrep})

def stats_view(request):
    return render(request, 'income/statistic.html')

