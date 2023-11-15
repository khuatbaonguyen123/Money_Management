from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Transaction
from moneym import models  
from django.db.models import Case, When, Sum, IntegerField, Q
from users.models import *
from moneym.models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def weekly_transactions(request):
    # Get the current date and the start date of the current week
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    

    # Initialize a dictionary to store data for each day
    transactions_by_day = []

    while start_of_week <= end_of_week:
        # Get transactions for the current day
        daily_transactions = Transaction.objects.filter(
            accountId__userId=request.user,
            dateCreated=start_of_week
        )

        # daily_transactions = daily_transactions.select_related('accountId')
        
        
        # Calculate total income and expense for the day
        total_income = daily_transactions.filter(type=1).aggregate(income=Sum('amount'))['income'] or 0
        total_expense = daily_transactions.filter(type=-1).aggregate(expense=Sum('amount'))['expense'] or 0

        # Calculate the daily total (income - expense)
        daily_total = total_income - total_expense

        # Append the data for the current day to the list
        transactions_by_day.append({
            'date': start_of_week,
            'transactions': daily_transactions,
            'daily_total': daily_total,
        })

        # Move to the next day
        start_of_week += timedelta(days=1)

    return render(request, 'moneym/weekly_transactions.html', {'transactions_by_day': transactions_by_day})

@login_required(login_url='/users/login')
def index(request):
    categories = Subcategory.objects.all()
    transactions = Transaction.objects.filter(accountId__userId=request.user, type=1)
    paginator = Paginator(transactions, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'transactions' : transactions,
        'page_obj': page_obj,
   }
    return render(request, 'income/index.html', context)
