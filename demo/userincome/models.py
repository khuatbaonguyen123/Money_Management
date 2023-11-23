from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Income(models.Model):
    amount = models.IntegerField(null=False, default=0)  # DECIMAL
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=266)


    def __str__(self):
        return self.source

    class Meta:
        ordering: ['-date']



