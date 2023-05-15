from django.db import models
from django.utils import timezone


class CarModel(models.Model):
    car_model_id = models.AutoField(primary_key=True)
    brand = models.CharField("Brand", max_length=100)
    car_model = models.CharField("Car model", max_length=100)
    year = models.DateField("Made on:", null=True)
    engine = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand} - {self.car_model}"

    class Meta:
        verbose_name = 'Car Model'
        verbose_name_plural = 'Car Models'


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    plate_nr = models.CharField(max_length=20)
    vin_number = models.CharField(max_length=17)
    client = models.CharField(max_length=100)
    photo = models.ImageField("Photo", upload_to="car_photos", null=True)

    def __str__(self):
        return f"{self.client} - {self.car_model} - {self.plate_nr} - {self.vin_number}"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.service_name}"

    class Meta:
        verbose_name = 'Services'
        verbose_name_plural = 'Services'


class ServicePrice(models.Model):
    service_price_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    cars = models.ManyToManyField(CarModel)
    price = models.FloatField("Price")

    def __str__(self):
        return f"{self.service} - {self.price}"

    class Meta:
        verbose_name = 'Service Price'
        verbose_name_plural = 'Service Prices'


# Uzsakymas
class OrderList(models.Model):
    order_list_id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(default=timezone.now)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.car} - {self.order_date} - {self.total_price}"

    class Meta:
        verbose_name = 'Order List'
        verbose_name_plural = 'Order Lists'


# Uzsakymo eilute
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_list_id = models.ForeignKey(OrderList, on_delete=models.SET_NULL, null=True, related_name="orders")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.order_list_id} - {self.service} - {self.quantity} - {self.price}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

