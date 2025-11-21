from django.contrib import admin
from .models import Product, Order, Collection

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','updated_at','inventory']
    list_per_page = 10
    search_fields = ['title','description']
    list_editable = ['price','inventory']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id','title']
