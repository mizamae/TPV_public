from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
import json
User=get_user_model()

from ProductsAPP.models import Product, ProductFamily

def home(request):
    product_families = ProductFamily.objects.all()
    
    return render(request, 'home_1.html',{'product_families':product_families})

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
