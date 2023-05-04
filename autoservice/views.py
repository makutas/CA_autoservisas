from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import generic
from .models import Car, CarModel, Service, Order, OrderList


def index(request):
    car_models = CarModel.objects.all().values('brand')
    car_model_count = CarModel.objects.count()
    services = Service.objects.all().values('service_name')
    services_count = Service.objects.count()

    context = {
        'car_models': car_models,
        'car_model_count': car_model_count,
        'services': services,
        'services_count': services_count
    }
    return render(request, 'index.html', context)


class CarListView(generic.ListView):
    model = Car
    paginate_by = 2
    template_name = "cars.html"


def specific_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    context = {'car': car}
    return render(request, "specific_car.html", context)


def services(request):
    all_services = Service.objects.all()
    context = {
        'services': all_services
    }
    return render(request, "services.html", context)


def orders(request):
    paginator = Paginator(OrderList.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_orders = paginator.get_page(page_number)
    return render(request, 'orders.html', {'orders': paged_orders})


def specific_order(request, order_list_id):
    order_list = get_object_or_404(OrderList, pk=order_list_id)
    orders_of_order_list = Order.objects.filter(order_list_id__exact=order_list_id)
    context = {'order_list': order_list, 'orders': orders_of_order_list}
    return render(request, "specific_order.html", context)

