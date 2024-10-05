from django.shortcuts import render
from rest_framework import viewsets, status  
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated  
from django.shortcuts import get_object_or_404  
#import stripe  
from .models import Subscription, PaymentHistory  
from .serializers import SubscriptionSerializer, PaymentHistorySerializer
from .utility import calculate_end_date, calculate_amount

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs): 
        interval = request.data.get('interval')
        amount = calculate_amount(interval)

        if Subscription.objects.filter(user=request.user, is_active=True).exists():  
            return Response({"error": "You can only have one active subscription at a time."},  
                            status=status.HTTP_400_BAD_REQUEST) 
        
        new_subscription = Subscription.objects.create(
            user = request.user,
            interval = interval,
            end_date=calculate_end_date(interval).date(),
            is_active = True,
        )   
        new_subscription.save()

        return Response(SubscriptionSerializer(new_subscription).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.is_active = False
        subscription.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  
        return PaymentHistory.objects.filter(subscription__user=self.request.user)
