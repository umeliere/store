from django.contrib import admin
from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'get_total_cost',)
    list_display = ('id', 'user', 'created', 'updated', 'full_name', 'cc_number', 'cc_expiry', 'cc_code')
    list_filter = ('paid', 'created', 'updated')
    inlines = [OrderItemInline]

    @staticmethod
    def get_total_cost(obj):
        return obj.get_total_cost()

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
