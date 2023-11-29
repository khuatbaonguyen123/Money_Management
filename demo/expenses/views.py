from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.db.models import Sum
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import datetime
from .models import Account


def search_expenses(request):
    if request.method == 'POST':
        try:
            search_str = json.loads(request.body).get('searchText')
            user_accounts = Account.objects.filter(user=request.user)
            expenses = Expense.objects.filter(
            amount__istartswith=search_str, account__in=user_accounts) | Expense.objects.filter(
            date__istartswith=search_str, account__in=user_accounts) | Expense.objects.filter(
            description__icontains=search_str, account__in=user_accounts) | Expense.objects.filter(
            category__name__icontains=search_str, account__in=user_accounts)
            # Note: Adjust the filtering conditions based on your model fields.
            data = list(expenses.values('amount', 'account__account_name', 'category__name', 'description', 'date'))
            return JsonResponse(data, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url='/authentication/login')
def index(request):
    accounts = Account.objects.filter(userId=request.user)
    
    expenses = Expense.objects.filter(account__in=accounts)

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
        category_id = request.POST['category']
        account_id = request.POST['account']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        account_instance = Account.objects.get(pk=account_id)
        category_instance = Category.objects.get(pk=category_id)
        expense = Expense.objects.create(account=account_instance, amount=amount, date=date,
                               category=category_instance, description=description)
        account_instance.balance -= int(expense.amount)
        account_instance.save()

        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    accounts = Account.objects.filter(userId=request.user)
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
        'accounts': accounts
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
        category_id = request.POST['category']
        account_id = request.POST['account']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        category_instance = Category.objects.get(pk=category_id)
        account_instance = Account.objects.get(pk=account_id)

        # Update expense fields
        expense.amount = amount
        expense.date = date
        expense.category = category_instance
        expense.description = description
        expense.account = account_instance

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    accounts = Account.objects.filter(userId=request.user)
    expenses = Expense.objects.filter(account__in=accounts,
                                      date__gte=six_months_ago, date__lte=todays_date)

    category_summary = expenses.values('category__name').annotate(total_amount=Sum('amount'))

    finalrep = {entry['category__name']: entry['total_amount'] for entry in category_summary}
    return JsonResponse({'expense_category_data': finalrep}, safe=False)
    


def stats_view(request):
    return render(request, 'expenses/stats.html')
