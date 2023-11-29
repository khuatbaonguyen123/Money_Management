from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Account(models.Model):
    account_name = models.CharField(max_length=255, null=False)
    balance = models.IntegerField(null=False, default=0)
    description = models.TextField(blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account_name} - {self.balance} - {self.description} - {self.userId}"
    
    class Meta:
        ordering = ['-account_name']