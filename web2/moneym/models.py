from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, CheckConstraint
from datetime import datetime
from users.models import *
class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.categoryId} - {self.name}"

class Subcategory(models.Model):
    subcategoryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    categoryId = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return f"{self.subcategoryId} - {self.categoryId} - {self.name}"

class Account(models.Model):
    accountId = models.AutoField(primary_key=True)
    accountName = models.CharField(max_length=255, null=False)
    type = models.IntegerField(choices=[(1, 'Cash'), (2, 'Bank Account'), (3, 'Credit Cards')], null=True)
    initialAmount = models.IntegerField(null=True)
    description = models.TextField(blank=True)
    userId = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.accountId} - {self.accountName} - {self.type} - {self.initialAmount} - {self.description} - {self.userId}"

class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    type = models.IntegerField(choices=[(1, 'Income'), (-1, 'Expense')])
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    accountId = models.ForeignKey(to=Account, on_delete=models.CASCADE, null=True)
    subcategoryId = models.ForeignKey(to=Subcategory, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(null=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering: ['-dateCreated']

    def __str__(self):
        return f"Transaction ID: {self.transactionId} - {self.amount}"

    
class Transfer(models.Model):
    transferId = models.AutoField(primary_key=True)
    fromAccountId = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='transfers_from')
    toAccountId = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='transfer_to')
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    amount = models.IntegerField(null=True)
    note = models.TextField(null=True)

    def __str__(self):
        return f"{self.transferId} - {self.amount}" 