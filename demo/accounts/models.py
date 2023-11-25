from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        (1, 'Cash'),
        (2, 'Bank Accounts'),
        (3, 'Cards'),
    ]
    accountName = models.CharField(max_length=255, null=False)
    type = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES, null=True)
    initialAmount = models.IntegerField(null=False, default=0)
    description = models.TextField(blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')

    def __str__(self):
        return f"{self.accountName} - {self.type} - {self.initialAmount} - {self.description} - {self.userId}"