from django.db import models
from django.contrib.auth.models import User
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
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.category.name

    class Meta:
        ordering = ['-date']


