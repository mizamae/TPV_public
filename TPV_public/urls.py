"""
URL configuration for TPV_public project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Import settings
from django.conf import settings

# Import static function 
from django.conf.urls.static import static  

from . import views

SERVER_PREPEND = ""

urlpatterns = [
    path(SERVER_PREPEND, views.home , name="home"),
    path('tracker/', views.tracker , name="tracker"),
    path(SERVER_PREPEND+'/ping/', views.ping , name="ping"),
    path('products/', include('ProductsAPP.urls')),
    path(SERVER_PREPEND+"/accounts/", include("django.contrib.auth.urls")),
    path(SERVER_PREPEND+'/admin/', admin.site.urls),
    path(SERVER_PREPEND+'/django_plotly_dash/', include('django_plotly_dash.urls')),
]

# Check DEBUG mode to adds additional URL patterns
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)