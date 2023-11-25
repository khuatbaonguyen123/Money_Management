from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Account(models.Model):
    account_name = models.CharField(max_length=255, null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.accountId} - {self.account_name} - {self.balance} - {self.description} - {self.userId}"