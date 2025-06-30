from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Column, Field
from crispy_forms.templatetags.crispy_forms_field import css_class

from django_recaptcha.fields import ReCaptchaField

FORMS_LABEL_CLASS='col'
FORMS_FIELD_CLASS='col'

class ContactForm(forms.Form):

    name = forms.CharField(label='Nombre',max_length=100,required = True)
    email = forms.EmailField(label='Email',required = True)
    phone = forms.CharField(label='Teléfono', max_length=12, required=False)
    message = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)