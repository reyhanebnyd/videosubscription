
from celery import shared_task  
from django.core.mail import send_mail  
from django.utils import timezone  
from datetime import timedelta  
from .models import Subscription  

@shared_task  
def deactivate_expired_subscriptions():  
    now = timezone.now()  
    expired_subscriptions = Subscription.objects.filter(end_date__lt=now, is_active=True)  
    for subscription in expired_subscriptions:  
        subscription.is_active = False  
        subscription.save()  

# @shared_task  
# def notify_users_about_expiration():  
#     notification_date = timezone.now() + timedelta(days=3)  
#     expiring_subscriptions = Subscription.objects.filter(end_date__date=notification_date.date(), is_active=True)  

#     for subscription in expiring_subscriptions:  
#         send_mail(  
#             subject='Subscription Expiration Notice',  
#             message=f'Your subscription will expire on {subscription.end_date}. Please renew to avoid losing access.',  
#             from_email='bonyadiho@gmail.com',  
#             recipient_list=[subscription.user.email],  
#         )