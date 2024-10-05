from rest_framework import serializers  
from .models import Subscription, PaymentHistory

class SubscriptionSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Subscription  
        fields = '__all__'  

class PaymentHistorySerializer(serializers.ModelSerializer):  
    class Meta:  
        model = PaymentHistory  
        fields = '__all__'  