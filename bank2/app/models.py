
from django.db import models

class BankAccount(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=80)
    account_no = models.BigIntegerField()
    balance = models.IntegerField(null=True, blank=True)
    pin = models.CharField(max_length=4,null=True, blank=True)
    photo = models.ImageField(upload_to='Images')  # New field for photo

    def __str__(self):
        return self.name
