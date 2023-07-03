from django.contrib import admin
from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'user',
                    'address', 'phone', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):

        if not change:
            obj.user = request.user

        super(OrderAdmin, self).save_model(
            request=request,
            obj=obj,
            form=form,
            change=change
        )
        

admin.site.register(Order, OrderAdmin)
