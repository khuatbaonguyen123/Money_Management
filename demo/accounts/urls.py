from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='account'),
    path('add-account', views.add_account, name='add-account'),
    path('edit-account/<int:id>', views.account_edit, name="account-edit")
]