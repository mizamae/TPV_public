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
DOCS_FILESYSTEM = FileSystemStorage(location=settings.MEDIA_ROOT)

import logging
logger = logging.getLogger("models")




class ProductType(models.Model):
    description = models.CharField(_("Description"), max_length=60, blank=True,null=True)

    def __str__(self):
        return self.description
    
class ProductAbstract(models.Model):

    NATURE_HW=0
    NATURE_SW = 1
    PRODUCT_NATURE = (
        (NATURE_HW, _("Hardware")),
        (NATURE_SW, _("Software")),
    )

    product_uuid = models.UUIDField(default=uuid.uuid4(), editable=False, primary_key = True)

    order = models.PositiveSmallIntegerField(verbose_name=_("Order"),default=0,editable = True)

    code = models.CharField(_("Code"), max_length=15, unique=True)
    card_title = models.CharField(_("Title in the card"), max_length=60, blank=True,null=True)
    card_text = models.TextField(_("Text in the card"), blank=True,null=True)
    card_image = models.ImageField(_("Image in the card"),blank=True,null=True,editable=True)

    type = models.ForeignKey(ProductType,verbose_name=_("Type of product"),help_text=_("Defines the nature of the product"),on_delete=models.CASCADE)
    nature = models.PositiveSmallIntegerField(verbose_name=_("Nature"),default=NATURE_HW,editable = True,choices=PRODUCT_NATURE)

    # DOCUMENTS
    externalview_code = models.CharField(verbose_name=_("Code to external views"),blank=True,null=True,editable=True)
    externalview_file = models.FileField(blank=True,null=True,editable=True)

    stepfile_code = models.CharField(verbose_name=_("Code to 3D step model"),blank=True,null=True,editable=True)
    stepfile_file = models.FileField(blank=True,null=True,editable=True)

    interfacesview_code = models.CharField(verbose_name=_("Code to interfaces views"),blank=True,null=True,editable=True)
    interfacesview_file = models.FileField(blank=True,null=True,editable=True)

    usermanual_code = models.CharField(verbose_name=_("Code to user manual"),blank=True,null=True,editable=True)
    usermanual_file = models.FileField(blank=True,null=True,editable=True)

    datasheet1_name = models.CharField(verbose_name=_("Name of the product of datasheet 1"),blank=True,null=True,editable=True)
    datasheet1_code = models.CharField(verbose_name=_("Code to datasheet 1"),blank=True,null=True,editable=True)
    datasheet1_file = models.FileField(blank=True,null=True,editable=True)

    datasheet2_name = models.CharField(verbose_name=_("Name of the product of datasheet 2"),blank=True,null=True,editable=True)
    datasheet2_code = models.CharField(verbose_name=_("Code to datasheet 2"),blank=True,null=True,editable=True)
    datasheet2_file = models.FileField(blank=True,null=True,editable=True)

    fw_code = models.CharField(verbose_name=_("Code to firmware"),blank=True,null=True,editable=True)
    fw_file = models.FileField(blank=True,null=True,editable=True)

    dbc_code = models.CharField(verbose_name=_("Code to dbc file"),blank=True,null=True,editable=True)
    dbc_file = models.FileField(blank=True,null=True,editable=True)

    binary_code = models.CharField(verbose_name=_("Code to binary file"),blank=True,null=True,editable=True)
    binary_file = models.FileField(blank=True,null=True,editable=True)

    class Meta:
        abstract = True
        
    def __str__(self):
        return self.code
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
    
    def updateFile(self,doc_code,file):
        updated_file=None
        if self.externalview_code == doc_code:
            if self.externalview_file!=file:
                ProductAbstract.deleteOldFile(file=self.externalview_file)
                self.externalview_file=file
                self.save(update_fields=['externalview_file'])
            updated_file="External views file"
        if self.stepfile_code == doc_code:
            if self.stepfile_file!=file:
                ProductAbstract.deleteOldFile(file=self.stepfile_file)
                self.stepfile_file=file
                self.save(update_fields=['stepfile_file'])
            updated_file='3D step file ' + self.stepfile_file.name.split(".")[0]
        if self.interfacesview_code == doc_code:
            if self.interfacesview_file!=file:
                ProductAbstract.deleteOldFile(file=self.interfacesview_file)
                self.interfacesview_file=file
                self.save(update_fields=['interfacesview_file'])
            updated_file='Interfaces views file'
        if self.usermanual_code == doc_code:
            if self.usermanual_file!=file:
                ProductAbstract.deleteOldFile(file=self.usermanual_file)
                self.usermanual_file=file
                self.save(update_fields=['usermanual_file'])
            updated_file='User manual ' + self.usermanual_file.name.split(".")[0]
        if self.fw_code == doc_code:
            if self.fw_file!=file:
                ProductAbstract.deleteOldFile(file=self.fw_file)
                self.fw_file=file
                self.save(update_fields=['fw_file'])
            updated_file='Firmware ' + self.fw_file.name.split(".")[0]
        if self.dbc_code == doc_code:
            if self.dbc_file!=file:
                ProductAbstract.deleteOldFile(file=self.dbc_file)
                self.dbc_file=file
                self.save(update_fields=['dbc_file'])
            updated_file='DBC file ' + self.dbc_file.name.split(".")[0]
        if self.datasheet1_code == doc_code:
            if self.datasheet1_file!=file:
                ProductAbstract.deleteOldFile(file=self.datasheet1_file)
                self.datasheet1_file=file
                self.save(update_fields=['datasheet1_file'])
            updated_file='Datasheet ' +self.datasheet1_name
        if self.datasheet2_code == doc_code:
            if self.datasheet2_file!=file:
                ProductAbstract.deleteOldFile(file=self.datasheet2_file)
                self.datasheet2_file=file
                self.save(update_fields=['datasheet2_file'])
            updated_file='Datasheet ' +self.datasheet2_name
        if self.binary_code == doc_code:
            if self.binary_file!=file:
                ProductAbstract.deleteOldFile(file=self.binary_file)
                self.binary_file=file
                self.save(update_fields=['binary_file'])
            updated_file='Release ' + self.binary_file.name.split(".")[0]
        
        if updated_file:
            receivers = signalProductUpdated.send(sender=self,updated_file=updated_file)
            recipients = []
            for receiver in receivers:
                if "signalProductUpdated_UsersAPP_receiver" in str(receiver[0]):
                    recipients =  receiver[1]
                    break

            sendNotificationEmail.delay(product_code=self.code,updated_file=updated_file,recipients=recipients)

    def getVideos(self):
        return self.videos.all().order_by('order')
    
    @staticmethod
    def deleteOldFile(file):
        try:
            if file.name:
                os.remove(file.path)
        except:
            logger.error("Error deleting file " + str(file))

    @staticmethod
    def getPathforFile(file):
        if isinstance(file,str):
            return os.path.join(settings.MEDIA_ROOT,file)
        else:
            return os.path.join(settings.MEDIA_ROOT,file.name)

    

class Product(ProductAbstract):
    @staticmethod
    def getAffectedInstances(doc_code):
        return Product.objects.filter(Q(externalview_code=doc_code) | Q(interfacesview_code=doc_code) | Q(usermanual_code=doc_code) |
                                      Q(fw_code=doc_code) | Q(dbc_code=doc_code) | Q(stepfile_code=doc_code) | Q(datasheet1_code=doc_code) | 
                                      Q(datasheet2_code=doc_code) | Q(binary_code=doc_code))
    

class VideoItem(models.Model):
    order = models.PositiveSmallIntegerField(verbose_name=_("Order"),default=0,editable = True)

    title = models.CharField(_("Title"), max_length=60, blank=True,null=True)
    text = models.TextField(_("Text describing the video"), blank=True,null=True)
    video_file = models.FileField(_("Video uploaded locally"),blank=True,null=True,editable=True)
    video_url = EmbedVideoField(_("Video from external server"),blank=True,null=True,editable=True)

    products = models.ManyToManyField(Product,related_name="videos")