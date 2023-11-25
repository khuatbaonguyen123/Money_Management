from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense, Account
# Create your views here.
from django.db.models import Sum, F
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import datetime
from .forms import ExpenseForm


def search_expenses(request):
    if request.method == 'POST':
        try:
            search_str = json.loads(request.body).get('searchText')
            expenses = Expense.objects.filter(
                amount__istartswith=search_str, account__userId=request.user
            ) | Expense.objects.filter(
                date__icontains=search_str, account__userId=request.user
            ) | Expense.objects.filter(
                description__icontains=search_str, account__userId=request.user
            ) | Expense.objects.filter(
                category__name__icontains=search_str, account__userId=request.user
            )

            # Note: Adjust the filtering conditions based on your model fields.

            data = list(expenses.values())
            return JsonResponse(data, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(account__userId=request.user)
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
    # context = {
    #     'categories': categories,
    #     'values': request.POST
    # }
    # if request.method == 'GET':
    #     return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        # amount = request.POST['amount']

        # if not amount:
        #     messages.error(request, 'Amount is required')
        #     return render(request, 'expenses/add_expense.html', context)
        # description = request.POST['description']
        # date = request.POST['date']
        # category = request.POST['category']

        # if not description:
        #     messages.error(request, 'description is required')
        #     return render(request, 'expenses/add_expense.html', context)

        # Expense.objects.create(owner=request.user, amount=amount, date=date,
        #                        category=category, description=description)
        # messages.success(request, 'Expense saved successfully')

        # return redirect('expenses')
        form = ExpenseForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses')
        else:
            return render(request, 'expenses/add_expense.html', {'categories': categories, 'form': form})
    else:
        form = ExpenseForm(request.user)
    return render(request, 'expenses/add_expense.html', {'categories': categories, 'form': form})


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    # expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    # context = {
    #     'expense': expense,
    #     'values': expense,
    #     'categories': categories
    # }
    # if request.method == 'GET':
    #     return render(request, 'expenses/edit-expense.html', context)
    # if request.method == 'POST':
    #     amount = request.POST['amount']

    #     if not amount:
    #         messages.error(request, 'Amount is required')
    #         return render(request, 'expenses/edit-expense.html', context)
    #     description = request.POST['description']
    #     date = request.POST['expense_date']
    #     category = request.POST['category']

    #     if not description:
    #         messages.error(request, 'description is required')
    #         return render(request, 'expenses/edit-expense.html', context)

    #     expense.owner = request.user
    #     expense.amount = amount
    #     expense. date = date
    #     expense.category = category
    #     expense.description = description

    #     expense.save()
    #     messages.success(request, 'Expense updated  successfully')

    #     return redirect('expenses')
    expense = get_object_or_404(Expense, id=id)
    form = ExpenseForm(request.user, request.POST or None, instance=expense)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')
    return render(request, 'expenses/edit-expense.html', {'form': form, 'expense': expense, 'categories': categories})


def delete_expense(request, id):
    # expense = Expense.objects.get(pk=id)
    # expense.delete()
    # messages.success(request, 'Expense removed')
    # return redirect('expenses')
    expense = get_object_or_404(Expense, id=id)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully')
        return redirect('expenses')

    return render(request, 'expenses/delete_expense.html', {'expense': expense})


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)

    user_accounts = Account.objects.filter(userId=request.user)
    expenses = Expense.objects.filter(account__in=user_accounts, date__range=(six_months_ago, todays_date))
    finalrep = {}

    # def get_category(expense):
    #     return expense.category
    # category_list = list(set(map(get_category, expenses)))

    # def get_expense_category_amount(category):
    #     amount = 0
    #     filtered_by_category = expenses.filter(category=category)

    #     for item in filtered_by_category:
    #         amount += item.amount
    #     return amount

    # for x in expenses:
    #     for y in category_list:
    #         finalrep[y] = get_expense_category_amount(y)
    # Use aggregation to get the sum of amounts for each category
    category_summary = expenses.values('category__name').annotate(total_amount=Sum('amount'))

    finalrep = {entry['category__name']: entry['total_amount'] for entry in category_summary}

    # Return the category-wise summary as JSON
    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')
