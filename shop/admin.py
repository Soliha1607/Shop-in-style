from django.contrib import admin
from shop.models import Product, Category

admin.site.register(Category)
if not admin.site.is_registered(Product):
    @admin.register(Product)
    class ProductAdmin(admin.ModelAdmin):
        class Media:
            css = {
                "all": ("admin/css/custom.css",)
            }



