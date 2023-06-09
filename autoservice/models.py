from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image


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
    description = HTMLField(null=True)

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
    due_back = models.DateField("Due back:", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def total_orderlist_price(self):
        total_sum = 0
        for order in self.orders.all():
            total_sum += order.total_order_price
        return total_sum

    def __str__(self):
        return f"{self.car} - {self.order_date} - {self.total_orderlist_price}"

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        verbose_name = 'Order List'
        verbose_name_plural = 'Order Lists'


# Uzsakymo eilute
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_list_id = models.ForeignKey(OrderList, on_delete=models.SET_NULL, null=True, related_name="orders")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    unit_price = models.FloatField()

    @property
    def total_order_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.order_list_id} - {self.service} - {self.quantity} - {self.unit_price}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderListComment(models.Model):
    order_list = models.ForeignKey(OrderList, on_delete=models.SET_NULL, null=True, blank=True, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Comment', max_length=2000)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = 'Comments'
        ordering = ['-date_created']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_picture.path)
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.profile_picture.path)
