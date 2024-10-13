# apps.py  
from django.apps import AppConfig  
from django.db.models.signals import post_migrate  

from django.dispatch import receiver  

class SubscriptionConfig(AppConfig):  
    default_auto_field = 'django.db.models.BigAutoField'  
    name = 'subscription'  

    def ready(self):  
        # Connect to the post_migrate signal to create periodic tasks  
        post_migrate.connect(create_periodic_task)  

@receiver(post_migrate)  
def create_periodic_task(sender, **kwargs):  
    if sender.name == 'subscription':    
        from .tasks import deactivate_expired_subscriptions  
        from django_celery_beat.models import IntervalSchedule, PeriodicTask  
        
        schedule, created = IntervalSchedule.objects.get_or_create(  
            every=24,  
            period=IntervalSchedule.HOURS,  
        )  

        PeriodicTask.objects.get_or_create(  
            interval=schedule,  
            name='Deactivate expired subscriptions',  
            task='subscription.tasks.deactivate_expired_subscriptions',  
        )

        # PeriodicTask.objects.create(  
        #     interval=schedule,  
        #     name='Notify users about subscription expiration',  
        #     task='subscription.tasks.notify_users_about_expiration',  
        # )