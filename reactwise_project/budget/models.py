from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date



class Expenses(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=30, default='approved')


class MoneySpent(models.Model):
    name = models.CharField(default='expense', max_length=100)
    spent = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)
    # auto_add_now=True fix at home


class Budget(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)
    

class Bot(models.Model):
    text = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)

