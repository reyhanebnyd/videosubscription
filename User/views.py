from django.shortcuts import render
from .serializers import SignUpSerializer
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.response import Response  
from rest_framework.permissions import AllowAny   
from .serializers import LoginSerializer, UserProfileSerializer, ChangePasswordSerializer
from .models import CustomUser, Profile
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import requests  
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter  
from dj_rest_auth.registration.views import SocialLoginView
from django.views import View  
from django.http import JsonResponse  
from allauth.socialaccount.providers.google.provider import GoogleProvider  
from allauth.socialaccount.models import SocialLogin, SocialAccount  
from allauth.socialaccount import *  
from rest_framework.views import APIView  
from requests.exceptions import RequestException
from allauth.socialaccount.adapter import get_adapter

class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (
        AllowAny,
    )
    serializer_class = SignUpSerializer

class LoginView(generics.GenericAPIView):  
    """  
    View for user login, allowing authentication via email, username, or phone number.  
    """  
    serializer_class = LoginSerializer  
    permission_classes = [AllowAny]   

    def post(self, request, *args, **kwargs):  
        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)  
        
         
        user = serializer.validated_data['user']  

          
        token = self.get_token_for_user(user)   

          
        return Response({  
            "message": "Login successful",  
             "token": token,    
            "user": {  
                "id": user.id,  
                "username": user.username,  
                "email": user.email,  
                # Add any additional user fields you want returned  
            }  
        }, status=status.HTTP_200_OK) 

    def get_token_for_user(self, user):  
        refresh = RefreshToken.for_user(user)  
        return {  
            'refresh': str(refresh),  
            'access': str(refresh.access_token),  
        }  

class UpdateProfileViewSet(viewsets.ModelViewSet):  
    permission_classes = [IsAuthenticated]  
    serializer_class = UserProfileSerializer  

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

    def create(self, request, *args, **kwargs):  
        return Response({'detail': 'Profile creation is not allowed.'}, status=status.HTTP_403_FORBIDDEN)  

    def destroy(self, request, *args, **kwargs):  
        return Response({'detail': 'Profile deletion is not allowed.'}, status=status.HTTP_403_FORBIDDEN)  

    def update(self, request, *args, **kwargs):  
        partial = kwargs.pop('partial', False)   
        instance = self.get_object()  
        serializer = self.get_serializer(instance, data=request.data, partial=partial)  
        serializer.is_valid(raise_exception=True)  
        self.perform_update(serializer)  

        return Response(serializer.data) 


# class GoogleLoginView(generics.GenericAPIView):  
#     serializer_class = GoogleLoginSerializer  
#     permission_classes = [AllowAny]  

#     def post(self, request, *args, **kwargs):  
#         serializer = self.get_serializer(data=request.data)  
#         serializer.is_valid(raise_exception=True)  

#         user = serializer.validated_data['user']  
#         token = self.get_token_for_user(user)  

#         return Response({  
#             "message": "Login successful",  
#             "token": token,  
#             "user": {  
#                 "id": user.id,  
#                 "username": user.username,  
#                 "email": user.email,  
#                 # Additional fields if needed  
#             }  
#         }, status=status.HTTP_200_OK)  

#     def get_token_for_user(self, user):  
#         refresh = RefreshToken.for_user(user)  
#         return {  
#             'refresh': str(refresh),  
#             'access': str(refresh.access_token),  
#         }  

class ChangePasswordView(generics.GenericAPIView):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = ChangePasswordSerializer
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({'success': True})        

class GoogleLogin(SocialLoginView):  
    adapter_class = GoogleOAuth2Adapter         


class GoogleOAuth2LoginView(APIView):  
    permission_classes = [AllowAny]  

    def post(self, request):  
        token = request.data.get("token")  # This is the Google OAuth token received  

        if not token:  
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)  

        # Verify token and get the user info from Google  
        user_info_endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"  
        headers = {"Authorization": f"Bearer {token}"}  
        
        user_info_response = requests.get(user_info_endpoint, headers=headers)  

        if user_info_response.status_code != 200:  
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)  

        user_info = user_info_response.json()  
        email = user_info.get("email")  

        if not email:  
            return Response({"error": "Email not found in user info"}, status=status.HTTP_400_BAD_REQUEST)  

        # Check if the user already exists  
        try:  
            user = CustomUser.objects.get(email=email)  
            social_account = SocialAccount.objects.filter(user=user, provider='google').first()  

            # If the account exists, authenticate the user  
            if social_account:  
                # Log the user in using complete_social_login from allauth  
                social_login = SocialLogin(user=user)  
                utils.complete_social_login(request, social_login)  
                return Response({"success": "User logged in successfully"}, status=status.HTTP_200_OK)  
            else:  
                return Response({"error": "User is not registered with Google."}, status=status.HTTP_400_BAD_REQUEST)  

        except CustomUser.DoesNotExist:  
            # If the user does not exist, we create a new user  
            user = CustomUser(email=email, username=email.split('@')[0])  
            user.set_unusable_password()  # If you don't need a password  
            user.save()  

            # Create a social account for the new user  
            SocialAccount.objects.create(user=user, provider='google', uid=user_info.get('sub'))  

            # Log the user in using complete_social_login  
            social_login = SocialLogin(user=user)  
            complete_social_login(request, social_login)  

            return Response({"success": "User registered and logged in successfully"}, status=status.HTTP_201_CREATED)  