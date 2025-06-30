from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
import json
User=get_user_model()

from ProductsAPP.models import Product, ProductFamily
from .forms import ContactForm

def home(request):
    product_families = ProductFamily.objects.all()
    contactForm = ContactForm()
    return render(request, 'home_1.html',{'product_families':product_families,'contactForm':contactForm})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.info(request, "Formulario recibido, nos pondremos en contacto contigo a la mayor brevedad posible")
        else:
            messages.warning(request, "Falta algún dato en el formulario")
        return redirect(reverse('home')+"#contact")
    else:
        return HttpResponse(status=404,content=json.dumps({}))


@ensure_csrf_cookie
def tracker(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        actiondata={}
        actionmodel=User.getActionModel()
        if 'media' in data['pathname']:
            actiondata['type']=actionmodel.ACTION_DOWNLOAD
            actiondata['data']={'file':data['pathname']}
        else:
            actiondata['type']=actionmodel.ACTION_CONSULT
            actiondata['data']={'destination':data['text'].strip()}
        actiondata['user']=request.user
        User.logAction(actiondata)
        return HttpResponse(status=201,content=json.dumps({}))
    else:
        return HttpResponse(status=404,content=json.dumps({}))
    
@ensure_csrf_cookie
def ping(request):
    if request.user.is_authenticated:
        return HttpResponse(status=200,content=json.dumps({}))
    else:
        return HttpResponse(status=404,content=json.dumps({}))
