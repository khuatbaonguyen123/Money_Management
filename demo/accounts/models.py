from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Account(models.Model):
    accountName = models.CharField(max_length=255, null=False)
    type = models.IntegerField(choices=[(1, 'Cash'), (2, 'Bank Accounts'), (3, 'Credit Cards')], null=True)
    initialAmount = models.IntegerField(null=False, default=0)
    description = models.TextField(blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.accountId} - {self.accountName} - {self.type} - {self.initialAmount} - {self.description} - {self.userId}"