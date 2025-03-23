from django.contrib.auth.models import BaseUserManager


# class Usermanagers(BaseUserManager):
#     def create_user(self,first_name,last_name,email, password ,**extra_fields):
#         user = self.model(first_name = first_name,
#                           last_name = last_name,
#                           email = email, password = password,
#                           **extra_fields
#                          )
#         user.set_password(password)
#         user.save()
#         return user
#     def create_superuser(self, first_name, last_name, email, 
#                           password, **extra_fields):
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(first_name, last_name, email, password)









class Usermanagers(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(first_name, last_name, email, password, **extra_fields)