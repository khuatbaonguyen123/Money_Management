from django.urls import path
from . import views

urlpatterns = [
    # path("transaction", views.transaction, name="transaction"),
    path("transaction/weekly", views.weekly_transactions,  name="weekly"),
    # path("transaction/monthly", views.monthly_transactions_view,  name="monthly"),
    path("transactions/index", views.index, name='index')
]