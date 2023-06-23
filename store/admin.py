from django.contrib import admin
from store import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('discount',)


@admin.register(models.Producer)
class ProducerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
