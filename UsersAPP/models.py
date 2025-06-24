from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import pytz

from rest_framework.authtoken.models import Token as AuthToken

from .managers import CustomUserManager


class User(AbstractUser):
    TYPE_SELLER=0
    TYPE_INTERNAL=10

    TYPES = (
        (TYPE_SELLER, _("[External] Seller")),
        (TYPE_INTERNAL, _("[Internal]")),        
    )

    type = models.PositiveSmallIntegerField(verbose_name=_("Type"),default=TYPE_SELLER,choices=TYPES)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        permissions=(
            ("access_manufacturingAPI", _("Can interact through the manufacturing API")),
        )

    def __str__(self):
        return self.username
    
    
    def shortName(self,):
        try:
            if self.first_name and self.last_name:
                return self.first_name[0]+"."+self.last_name
            else:
                values = self.username.split(".")
                return values[0][0].upper()+"."+values[1].capitalize()
        except:
            return str(self)
                
    def getGroups(self,):
        return self.groups.all()

    @admin.display(description=_("Profiles"))
    def printGroups(self,):
        groups=self.getGroups()
        if groups:
            if len(groups) == 1:
                return str(groups[0])
            else:
                listgroups=str(groups[0])
            for group in groups[1:]:
                listgroups+=", "+str(group)
            return listgroups
        else:
            return ""


    def deleteToken(self):
        from rest_framework.authtoken.models import Token
        token = Token.objects.get(user_id=self.id)
        token.delete() 
        
    @admin.display(description=_("Type"))
    def getType(self) -> str:
        return self.get_type_display()
    
                    

