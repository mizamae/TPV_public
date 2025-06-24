

from celery import shared_task
from django.conf import settings
from django.template.loader import get_template

from django.contrib.staticfiles import finders
import os
import logging
logger = logging.getLogger("celery")

@shared_task(bind=False,name='UsersAPP_sendNotificationEmail')
def sendNotificationEmail(product_code,updated_file,recipients):

    attachment = finders.find('logos/email.png')

    message = get_template("ProductsAPP/_notificationmail_template.html").render({
        'heading': "This email is to advise of an update in the documentation of the product " + product_code,
        'product_code':product_code,
        'image':os.path.basename(attachment),
        'link':"https://"+settings.PAGE_DNS,
        'changed':updated_file,
    })



    subject = "Notification of product update from NX-technologies"
    
    if "gmail" in settings.EMAIL_HOST:
        from utils.googleGmail import googleGmail_handler
        googleGmail_handler.sendMultipleEmails(subject=subject,attachments=(attachment,),recipients=recipients,html_content=message)
    elif "office365" in settings.EMAIL_HOST:
        from utils.microsoft365 import Microsoft365_handler
        Microsoft365_handler.sendEmail(subject=subject,attachments=(attachment,),recipients=recipients,html_content=message)