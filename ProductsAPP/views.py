from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from itertools import chain

import os
import json
import base64
import io

from .models import Product, ProductFamily
# Create your views here.

import logging
logger = logging.getLogger("users")

@csrf_exempt
def updateFamily(request):
    if request.method == 'POST':
        url = request.build_absolute_uri()
        logger.info("Request to update family from origin: " + str(url))
        
        from itsdangerous.serializer import Serializer
        s = Serializer(settings.SIGNATURE_KEY)

        req_info = json.load(request)
        sig_okay, payload = s.loads_unsafe(req_info)
        
        if sig_okay:
            try:
                #print(str(payload))
                payload=json.loads(payload)
                created = False
                try:
                    family = ProductFamily.objects.get(id=payload['id'])
                except ProductFamily.DoesNotExist:
                    created = True
                    family = ProductFamily.objects.create(**{'id':payload['id'],'name':payload['name'],
                                                           'short_description':payload['short_description'],
                                                           'long_description':payload['long_description']})

                if payload.get('image',None):            
                    data = base64.b64decode(bytes(payload['image'], 'utf-8'))
                    file = 'family'+str(payload['id'])+payload['image_extension']
                    
                    temp_thumb = io.BytesIO(data)
                    family.image.save(
                        file,
                        temp_thumb,
                        save=True,
                    )
                if not created:
                    family.name=payload['name']
                    family.short_description=payload['short_description']
                    family.long_description=payload['long_description']
                    family.save()
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=201)
            except Exception as ex:
                logger.error(str(ex))
                return HttpResponse(status=500)
        else:
            logger.error("Invalid request signature")
            return HttpResponse(status=500)

    else:
        return HttpResponse(status=500)


@csrf_exempt
def updateProduct(request):
    if request.method == 'POST':
        url = request.build_absolute_uri()
        logger.info("Request to update product from origin: " + str(url))
        
        from itsdangerous.serializer import Serializer
        s = Serializer(settings.SIGNATURE_KEY)

        req_info = json.load(request)
        sig_okay, payload = s.loads_unsafe(req_info)
        
        if sig_okay:
            try:
                #print(str(payload))
                payload=json.loads(payload)
                created = False
                try:
                    product = Product.objects.get(id=payload['id'])
                except Product.DoesNotExist:
                    created = True
                    product = Product.objects.create(**{'id':payload['id'],
                                                            'name':payload['name'],
                                                            'family':ProductFamily.objects.get(id=payload['family']),
                                                           'details':payload['details'],
                                                           'stock':payload['stock'],
                                                           'discount':payload['discount'],
                                                           'promotion':payload['promotion'],
                                                           'pvp':payload['pvp']})
                    
                
                if payload.get('image',None):            
                    data = base64.b64decode(bytes(payload['image'], 'utf-8'))
                    file = 'product'+str(payload['id'])+payload['image_extension']
                    temp_thumb = io.BytesIO(data)
                    product.image.save(
                        file,
                        temp_thumb,
                        save=True,
                    )

                if not created:
                    product.name=payload['name'] if payload.get('name',None) else product.name
                    product.details=payload['details'] if payload.get('details',None) else product.details
                    product.stock=payload['stock'] if payload.get('stock',None) else product.stock
                    product.discount=payload['discount'] if payload.get('discount',None) else product.discount
                    product.promotion=payload['promotion'] if payload.get('promotion',None) else product.promotion
                    product.pvp=payload['pvp'] if payload.get('pvp',None) else product.pvp
                    product.save()
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=201)
                
            except Exception as ex:
                logger.error(str(ex))
                return HttpResponse(status=500)
        else:
            logger.error("Invalid request signature")
            return HttpResponse(status=500)

    else:
        return HttpResponse(status=500)


    
def viewProduct(request,product_uuid):
    product = get_object_or_404(Product, product_uuid=product_uuid)
    if not request.user.canSeeProduct(code=product.code):
        return redirect('UsersAPP_permissionDenied')
    
    return render(request, 'ProductsAPP/_product2.html',{'navbartitle':_("Product " + str(product.code)),
                                                         'product':product,
                                                          })

def downloadUsermanual(request,product_uuid):
    product = get_object_or_404(Product, product_uuid=product_uuid)
    if not request.user.canSeeProduct(code=product.code):
        return redirect('UsersAPP_permissionDenied')
    
    file = os.path.join(settings.FILE_DIR,"usermanual.pdf")
    file_name = os.path.basename(file)
    with open(file, "rb") as f:
        response = HttpResponse(f.read(),content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name

    return response


    