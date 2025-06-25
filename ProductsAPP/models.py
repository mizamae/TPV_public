from django.contrib import admin
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from embed_video.fields import EmbedVideoField

import os 
import uuid

from .signals import signalProductUpdated
from .tasks import sendNotificationEmail

FILE_DIR = os.path.join(settings.MEDIA_ROOT)
IMAGES_FILESYSTEM = FileSystemStorage(location=FILE_DIR,base_url=settings.MEDIA_URL)


import logging
logger = logging.getLogger("models")


class ProductFamily(models.Model):
    name = models.CharField(_("Nombre"), max_length=30,unique=True)
    image = models.ImageField(_("Imagen"),upload_to=settings.MEDIA_ROOT)
    short_description = models.CharField(_("Descripción breve"), max_length=300)
    long_description = models.TextField(_("Descripción detallada"))

    def __str__(self):
        return self.name
    
class Product(models.Model):

    name = models.CharField(_("Nombre"), max_length=60)
    image = models.ImageField(_("Imagen"),upload_to=settings.MEDIA_ROOT)
    details = models.CharField(_("Descripción breve"), max_length=300)
    family = models.ForeignKey(ProductFamily,on_delete=models.CASCADE,related_name='products',verbose_name=_("Familia de producto"))
    pvp = models.FloatField(verbose_name=_("Precio de venta"),help_text=_("Precio de venta de una unidad"))
    stock = models.FloatField(verbose_name=_("Cantidad en stock"),blank=True,default=0)
    discount = models.CharField(blank=True,null=True, max_length=10)
    promotion = models.CharField(blank=True,null=True, max_length=10)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
    