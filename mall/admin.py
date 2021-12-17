from django.contrib import admin
from .models import Product, Maker, Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product)
admin.site.register(Maker)
admin.site.register(Category, CategoryAdmin)
