from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class CalSpending(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)
