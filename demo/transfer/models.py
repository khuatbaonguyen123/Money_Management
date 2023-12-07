# models.py in your transfer app

from django.db import models
from accounts.models import Account

class Transfer(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_from')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_to')
    amount = models.IntegerField(null=False, default=0)  # DECIMAL
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"Transfer from {self.from_account} to {self.to_account} - Amount: {self.amount}"
