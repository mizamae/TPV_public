from django.contrib import admin

from .models import VideoItem,ProductType, Product

class VideoItemAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(VideoItem, VideoItemAdmin)

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('description',)

admin.site.register(ProductType, ProductTypeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("order","code","type","nature")
    ordering = ("type",'order')

admin.site.register(Product, ProductAdmin)