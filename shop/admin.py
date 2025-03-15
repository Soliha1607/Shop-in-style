from django.contrib import admin
from shop.models import Product, Category, Comment, Orders

admin.site.register(Orders)
admin.site.register(Comment)
admin.site.register(Category)
if not admin.site.is_registered(Product):
    class ProductAdmin(admin.ModelAdmin):
        list_display = ('name', 'category', 'price')

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == "category":
                kwargs["queryset"] = Category.objects.all()
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

    admin.site.register(Product, ProductAdmin)
