from django.core import mail
from django.conf import settings
from email.mime.image import MIMEImage
import os
import logging
logger = logging.getLogger("models")

class googleGmail_handler(object):

    @staticmethod
    def attachment_data(attachment):
        with open(attachment, 'rb') as f:
            logo_data = f.read()
        logo = MIMEImage(logo_data)
        filename = str(os.path.basename(attachment)) # be carefull with the filename. It seems it does not work if "logo" is oncluded in the filename
        logo.add_header('Content-Disposition', 'attachment',filename=filename)
        return logo

    @staticmethod
    def sendEmail(subject,recipient,html_content,attachments=None):

        email = mail.EmailMessage(
                subject=subject,
                body=html_content,
                from_email=settings.EMAIL_HOST_USER,
                to=(recipient,),
                reply_to=[],
            )
        email.content_subtype = "html"

        if attachments:
            for attachment in attachments:
                email.attach(googleGmail_handler.attachment_data(attachment))
        email.send()

        logger.info("Confirmation email sent to " + str(recipient))
    
    @staticmethod
    def sendMultipleEmails(subject,recipients,html_content,attachments=None):
        connection = mail.get_connection()
        emails=[]

        # this sends individual mails to each recipient so that does not disclose the addresses
        for recv in recipients:
            email = mail.EmailMessage(
                                            subject=subject,
                                            body=html_content,
                                            from_email=settings.EMAIL_HOST_USER,
                                            to=[recv,],
                                            bcc=[],
                                            reply_to=[],
                                            connection=connection,
                                        )
            email.content_subtype = "html"
            if attachments:
                for attachment in attachments:
                    email.attach(googleGmail_handler.attachment_data(attachment))
            emails.append(email)
               
        # Send the two emails in a single call -
        connection.send_messages(emails)
        # The connection was already open so send_messages() doesn't close it.
        # We need to manually close the connection.
        connection.close()

        logger.info("Notification email sent to " + str(recipients))