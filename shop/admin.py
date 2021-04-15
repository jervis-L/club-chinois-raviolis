from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price','category','dt_info', 'created']
    list_filter = ['price','created', 'category']
    list_editable = ['price', 'dt_info','category']
    prepopulated_fields = {'slug': ('name',)}
    
admin.site.register(Product, ProductAdmin)
