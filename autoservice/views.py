from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Car, CarModel, Service, Order, OrderList
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import User


def index(request):
    car_models = CarModel.objects.all().values('brand')
    car_model_count = CarModel.objects.count()
    services = Service.objects.all().values('service_name')
    services_count = Service.objects.count()
    num_visits = request.session.get('num_visits', 1)

    context = {
        'car_models': car_models,
        'car_model_count': car_model_count,
        'services': services,
        'services_count': services_count,
        'num_visits': num_visits,
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


def search_cars(request):
    query = request.GET.get('query')
    search_results = Car.objects.filter(Q(client__icontains=query) | Q(car_model__car_model__icontains=query)
                                        | Q(car_model__brand__icontains=query) | Q(plate_nr__icontains=query)
                                        | Q(vin_number__icontains=query))
    return render(request, 'search_cars.html', {'cars': search_results, 'query': query})


@login_required(login_url='login')
def user_orders(request):
    try:
        user_orderlists = OrderList.objects.filter(reader=request.user).filter(book_status__exact='t').order_by('due_back')
    except OrderList.DoesNotExist:
        user_orderlists = None

    context = {
        'user': request.user,
        'user_books': user_orderlists,
    }

    return render(request, 'user_orderlists.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":
        # Retrieve values from the form via POST request
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if the original and repeated passwords match
        if password != password2:
            messages.error(request, 'The passwords do not match!')
            return redirect('register')

        # Check if username is taken
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username {username} is taken!')
            return redirect('register')

        # Check if email is taken
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email {email} is taken!')
            return redirect('register')

        # If the checks are passed, we can create a new User
        User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                 email=email, password=password)

        messages.info(request, f'User {username} registered successfully!')
        return redirect('login')

    return render(request, 'registration/register.html')