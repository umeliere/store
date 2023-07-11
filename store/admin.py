from django.contrib import admin
from store.models import Product, Producer, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('discount',)


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
