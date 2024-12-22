from django.db import models

from .constants import TRANSACTION_TYPE_CHOICES
from accounts.models import UserBankAccount


class Transaction(models.Model):
    account = models.ForeignKey(
        UserBankAccount,
        related_name='transactions',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    description = models.TextField(blank=True)
    ##Transfer
    
    source_account = models.CharField(max_length=100,blank=True)
    destination_account = models.CharField(max_length=100,blank=True)
    
    # Payment
    recipient_name = models.CharField(max_length=100,blank=True)
    recipient_account = models.CharField(max_length=100,blank=True)
    payment_method = models.CharField(max_length=20,blank=True, choices=[
        ('credit_card', 'Credit Card'),
        ('bank_account', 'Bank Account')
    ])
    

    def __str__(self):
        return str(self.account.account_no)

    class Meta:
        ordering = ['timestamp']


## FD and RD

# your_app/models.py

from django.db import models
from django.conf import settings  # Import settings

class FDApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.PositiveIntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FD Application by {self.user.username} - {self.status}"

class RDApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.PositiveIntegerField()  # in months
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RD Application by {self.user.username} - {self.status}"
    




class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.first_name}'









