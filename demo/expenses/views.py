from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
# Create your views here.
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import datetime
from .models import Account


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        user_accounts = Account.objects.filter(userId=request.user)
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, account__in=user_accounts) | Expense.objects.filter(
            date__istartswith=search_str, account__in=user_accounts) | Expense.objects.filter(
            description__icontains=search_str, account__in=user_accounts) | Expense.objects.filter(
            category__icontains=search_str, account__in=user_accounts)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    accounts = Account.objects.filter(userId=request.user)
    
    expenses = Expense.objects.filter(account__in=accounts).order_by('-date')

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    accounts = Account.objects.filter(userId=request.user)
    context = {
        'categories': categories,
        'accounts' : accounts,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        account_id = request.POST['account']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        account_instance = Account.objects.get(pk=account_id)
        expense = Expense.objects.create(account=account_instance, amount=amount, date=date,
                               category=category, description=description)
        account_instance.balance -= int(expense.amount)
        account_instance.save()

        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')


def expense_category_summary(request):
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
    expenses = Expense.objects.filter(account__in=accounts,
                                      date__gte=start_date, date__lte=end_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')
