from django.shortcuts import render, redirect
from .models import Source, Income
from django.db.models import Sum
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
        user_accounts = Account.objects.filter(user=request.user)
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
        source_id = request.POST['source']
        account_id = request.POST['account']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add_income.html', context)

        account_instance = Account.objects.get(pk=account_id)
        source_instance = Source.objects.get(pk=source_id)
        income = Income.objects.create(account=account_instance, amount=amount, date=date,
                               source=source_instance, description=description)
        
        # Update the balance of the associated account
        account_instance.balance += int(income.amount)
        account_instance.save()

        messages.success(request, 'Income saved successfully')

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
        source_id = request.POST['source']
        account_id = request.POST['account']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)
        account_instance = Account.objects.get(pk=account_id)
        source_instance = Source.objects.get(pk=source_id)

        income.amount = amount
        income. date = date
        income.source = source_instance
        income.description = description
        income.account = account_instance

        income.save()
        messages.success(request, 'Income updated  successfully')

        return redirect('income')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed')
    return redirect('income')

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)

    accounts = Account.objects.filter(userId=request.user)
    income = Income.objects.filter(account__in=accounts, date__gte=six_months_ago, date__lte=todays_date)

    source_summary = income.values('source__name').annotate(total_amount=Sum('amount'))

    finalrep = {entry['source__name']: entry['total_amount'] for entry in source_summary}

    # Return the category-wise summary as JSON
    return JsonResponse({'income_source_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'income/statistic.html')

