from django.db import models
import datetime


class CarModel(models.Model):
    car_model_id = models.AutoField(primary_key=True)
    brand = models.CharField("Brand", max_length=100)
    car_model = models.CharField("Car model", max_length=100)
    year = models.DateField("Made on:", null=True)
    engine = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand} - {self.car_model}"

    # TODO - Class Meta: verbose_name+plural


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    plate_nr = models.CharField(max_length=20)
    vin_number = models.CharField(max_length=200)
    client = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.client} - {self.car_model} - {self.plate_nr} - {self.vin_number}"


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.service_name}"


class ServicePrice(models.Model):
    service_price_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    cars = models.ManyToManyField(CarModel)
    price = models.FloatField("Price")

    def __str__(self):
        return f"{self.service} - {self.price}"

    # TODO - prideti manytomany fielda i admina per atskira methoda


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(default=datetime.datetime.now())
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.car} - {self.total_price} - {self.order_date}"


class OrderList(models.Model):
    order_list_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.service} - {self.quantity} - {self.price}"
