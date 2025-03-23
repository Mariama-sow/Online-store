from django.contrib.auth.backends import ModelBackend

from .models import User

# class CustomAuthentication(ModelBackend):
#     def authenticate(self, request, username , email, password):
#         try:
#             user = User.objects.get(email = username)
#         except User.DoesNotExist:
#             return None
#         if user.check_password(password):
#             request.user = user
#             return user
#         return None
    

class CustomAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None