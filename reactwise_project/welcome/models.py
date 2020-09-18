from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.BigIntegerField()
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
