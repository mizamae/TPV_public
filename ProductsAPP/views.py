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

from .models import Product
# Create your views here.

import logging
logger = logging.getLogger("users")

@csrf_exempt
def updateProduct(request):
    if request.method == 'POST':
        url = request.build_absolute_uri()
        logger.info("Request to update product from origin: " + str(url))

        if 'https' in url:
            return HttpResponse(status=500,content='Invalid operation')
        
        from itsdangerous.serializer import Serializer
        s = Serializer(settings.SIGNATURE_KEY)

        req_info = json.load(request)
        sig_okay, payload = s.loads_unsafe(req_info['signature'])
        
        if sig_okay:
            try:
                #print(str(payload))
                payload=json.loads(payload)
                doc_code = payload['code']
                doc_name = payload['name']
                doc_extension = payload['extension']
                logger.info("Request to update: " + str(doc_code))
                products = list(chain(Product.getAffectedInstances(doc_code=doc_code),CustomerProduct.getAffectedInstances(doc_code=doc_code)))
                logger.info("Products affected: " + str(products))
                if products == []:
                    return HttpResponse(status=404)
                
                data = base64.b64decode(bytes(payload['content'], 'utf-8'))
                file=Product.getPathforFile(doc_name)
                with open(file, "wb") as writer:
                    writer.write(data)

                for product in products:
                    product.updateFile(doc_code=doc_code,file=doc_name)

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


    