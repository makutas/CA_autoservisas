from django.urls import path

from . import views

urlpatterns = [
    # INDEX
    path('', views.index, name='index'),
    # PAGE TO DISPLAY ALL CARS IN SERVICE
    path('cars/', views.cars, name='cars'),
    # DETAIL DISPLAY OF CAR
    path('cars/<int:car_id>', views.specific_car, name='specific_car'),
    # ALL SERVICES
    path('services/', views.services, name='services'),
    # ALL ORDERS
    path('orders/', views.orders, name='orders'),
    # SPECIFIC ORDER
    path('orders/<int:order_list_id>/', views.specific_order, name='specific_order'),
]
