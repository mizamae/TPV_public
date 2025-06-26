from django.urls import path
from . import views

urlpatterns = [
    path("updatefamily", views.updateFamily, name="ProductsAPP_updatefamily"),
    path("deletefamily", views.deleteFamily, name="ProductsAPP_deletefamily"),
    path("updateproduct", views.updateProduct, name="ProductsAPP_updateproduct"),
    path("deleteproduct", views.deleteProduct, name="ProductsAPP_deleteproduct"),
    path("view/<str:product_uuid>",views.viewProduct, name="ProductsAPP_viewproduct"),
]