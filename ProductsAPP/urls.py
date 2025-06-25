from django.urls import path
from . import views

urlpatterns = [
    path("updatefamily", views.updateFamily, name="ProductsAPP_updatefamily"),
    path("updateproduct", views.updateProduct, name="ProductsAPP_updateproduct"),
    path("view/<str:product_uuid>",views.viewProduct, name="ProductsAPP_viewproduct"),
]