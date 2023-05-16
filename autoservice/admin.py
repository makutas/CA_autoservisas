from django.contrib import admin
from .models import CarModel, Car, Service, ServicePrice, Order, OrderList, OrderListComment


class OrderInline(admin.TabularInline):
    model = Order
    # turn off extra empty lines for inputs
    extra = 0


class OrderListAdmin(admin.ModelAdmin):
    list_display = ('car', 'order_date', 'due_back', 'user')
    inlines = [OrderInline]


class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'car_model', 'plate_nr', 'vin_number')
    list_filter = ('client', 'car_model')
    search_fields = ('plate_nr', 'vin_number')


class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ('service', 'price')


class OrderListCommentAdmin(admin.ModelAdmin):
    list_display = ('order_list', 'commenter', 'date_created', 'content')


admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(Service)
admin.site.register(ServicePrice)
admin.site.register(OrderList, OrderListAdmin)
admin.site.register(Order)
admin.site.register(OrderListComment, OrderListCommentAdmin)
