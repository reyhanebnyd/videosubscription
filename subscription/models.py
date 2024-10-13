from django.db import models
from User.models import CustomUser

class Subscription(models.Model):
    CHOICES={
        ('m', 'Monthly'),
        ('s', '3 Month'),
        ('h', '6 Month'),
        ('y', 'yearly'),
    }
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    is_active = models.BooleanField(null=False, blank=False, default=False)
    start_date = models.DateField(null=False, blank=False, auto_now_add=True)
    end_date = models.DateField()
    interval = models.CharField(max_length=1 ,choices=CHOICES)

class PaymentHistory(models.Model):
    CHOICES={
        ('s', 'Success'),
        ('p', 'Pending'),
        ('f', 'Failed'),
    }
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=CHOICES)
    


