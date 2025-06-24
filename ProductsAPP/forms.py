from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings

#from .constants import BUCKET_TEMPLATES_OPTIONS
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions,AppendedText, Accordion, AccordionGroup,UneditableField, InlineField
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Column, Field,Fieldset
from crispy_forms.templatetags.crispy_forms_field import css_class

import datetime
FORMS_LABEL_CLASS='col-4'
FORMS_FIELD_CLASS='col-8'

