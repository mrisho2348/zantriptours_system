from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from tourOrderingApp.models import CustomUser

class EmailBackend(ModelBackend):
    def authenticate(self,username=None,password=None,**kwargs):
        UserModel = get_user_model()
        try:
            user = CustomUser.objects.get(email=username,)
            
        except CustomUser.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None    
                
    

