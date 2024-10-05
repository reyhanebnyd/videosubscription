from django.shortcuts import render
from .serializers import SignUpSerializer
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.response import Response  
from rest_framework.permissions import AllowAny   
from .serializers import LoginSerializer
from .models import CustomUser
from rest_framework import status



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