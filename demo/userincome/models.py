from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from accounts.models import *

# Create your models here.
class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Income(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    amount = models.FloatField()  
    date = models.DateField(default=now)
    description = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE, default=1)
    


    def __str__(self):
        return self.source

    class Meta:
        ordering: ['-date']


