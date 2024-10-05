from django.contrib.auth.backends import ModelBackend  
from .models import CustomUser  

class EmailOrPhoneOrUsernameBackend(ModelBackend):  
    def authenticate(self, request, identifier=None, password=None, **kwargs): 
        try:  
            if "@" in identifier:  
                # Authenticate by email  
                user = CustomUser.objects.get(email=identifier)  
            else:  
                try:  
                    # Authenticate by username  
                    user = CustomUser.objects.get(username=identifier)  
                except CustomUser.DoesNotExist:  
                    # Authenticate by phone number  
                    user = CustomUser.objects.get(phone_number=identifier)  

            # Check the password  
            if user.check_password(password):  
                return user  
        except CustomUser.DoesNotExist:  
            return None  