from django.shortcuts import render
from rest_framework import viewsets, status  
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated  
from django.shortcuts import get_object_or_404  
from .models import Subscription, PaymentHistory  
from .serializers import SubscriptionSerializer, PaymentHistorySerializer
from .utility import calculate_end_date, calculate_amount
import random
import string
from datetime import datetime

class SubscriptionViewSet(viewsets.ViewSet):  
    permission_classes = [IsAuthenticated]  

    def retrieve(self, request, pk=None):   
        try:  
            subscription = Subscription.objects.get(pk=pk, user=request.user, is_active=True)  
        except Subscription.DoesNotExist:  
            return Response({"error": "Subscription not found or you do not have permission to view it."},   
                            status=status.HTTP_404_NOT_FOUND)  

 
        days_left = (subscription.end_date - datetime.now().date()).days  

       
        subscription_data = SubscriptionSerializer(subscription).data  
        subscription_data['days_left'] = days_left  

        return Response(subscription_data, status=status.HTTP_200_OK)  

    def create(self, request):  
        token = request.data.get('token')   
        interval = request.data.get('interval')  

     
        if not token:  
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)  

        if Subscription.objects.filter(user=request.user, is_active=True).exists():  
            return Response({"error": "You can only have one active subscription at a time."},   
                            status=status.HTTP_400_BAD_REQUEST)  

   
        new_subscription = Subscription.objects.create(  
            user=request.user,  
            interval=interval,  
            end_date=calculate_end_date(interval),  
            is_active=True,  
        )  
        new_subscription.save()  
        amount = calculate_amount(interval)
        
        PaymentHistory.objects.create(  
            subscription=new_subscription,  
            amount=amount,   
            payment_status='s',   
          
        )  
 
        return Response(SubscriptionSerializer(new_subscription).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):  
        
        try:  
            subscription = Subscription.objects.get(pk=pk, user=request.user, is_active=True)  
        except Subscription.DoesNotExist:  
            return Response({"error": "Subscription not found or you do not have permission to delete it."},   
                            status=status.HTTP_404_NOT_FOUND)  

 
        subscription.is_active = False  
        subscription.save()  

        return Response({"message": "Subscription has been successfully deleted."}, status=status.HTTP_204_NO_CONTENT) 
    
  




class MockPaymentViewSet(viewsets.ViewSet):  
    permission_classes = [IsAuthenticated]  

    def create(self, request):  
        interval = request.data.get('interval')  
        card_info = request.data.get('card_info')  

     
        if not interval or not card_info:  
            return Response({"error": "interval and card information required."}, status=status.HTTP_400_BAD_REQUEST)  

        
        token = self.generate_random_token(30)  

        return Response({"token": token}, status=status.HTTP_200_OK)  

    def generate_random_token(self, length):  
        characters = string.ascii_letters + string.digits  
        return ''.join(random.choice(characters) for _ in range(length)) 