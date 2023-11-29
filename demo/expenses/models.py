from django.db import models
from accounts.models import Account
from django.utils.timezone import now
from accounts.models import *

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.IntegerField()
    date = models.DateField(default=now)
    description = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE,default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.category)

    class Meta:
        ordering = ['-date']