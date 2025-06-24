from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self,**extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not 'username' in extra_fields or extra_fields['username'] =='':
            raise ValueError(_("The username must be set"))
        
        user = self.model(**extra_fields)
        user.set_password(extra_fields['password'])
        user.save()
        return user
    
    def create_superuser(self, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("type", self.model.TYPE_INTERNAL)

        return self.create_user(**extra_fields)