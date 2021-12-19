from django.contrib import admin
from .models import Product, Maker, Category, Comment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
#admin.site.register(Product, MarkdownxModelAdmin)
admin.site.register(Comment)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product)
admin.site.register(Maker)
admin.site.register(Category, CategoryAdmin)
