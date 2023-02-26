import email
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime, date


# Create your models here.


from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    house_address = models.CharField(max_length=200, null=True, blank=True)
    products_bought = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # calculate age from dob and save to age attribute
        if self.dob:
            today = date.today()
            age = today.year - self.dob.year - \
                ((today.month, today.day) < (self.dob.month, self.dob.day))
            self.age = age
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=200, choices=(
        ('Auckland', 'Auckland'),
        ('Christchurch', 'Christchurch'),
        ('Queenstown', 'Queenstown'),
    ), default='Auckland')
    quantity = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    delivery_method = models.CharField(max_length=50, null=True, blank=True)
    shipping_charge = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        if self.customer:
            # apply discount based on customer type and purchase details
            if self.customer.dob and (datetime.now().year - self.customer.dob.year) > 60:
                total -= total * Decimal('0.1')  # apply 10% senior discount
            if self.date_ordered.weekday() in [5, 6]:
                total -= total * Decimal('0.02')  # apply 2% weekend discount
            if self.customer.location in ['Auckland', 'Wellington']:
                total -= total * Decimal('0.01')  # apply 1% location discount
        if self.delivery_method == 'courier':
            # add $10 shipping charge for courier delivery
            total += Decimal('10.0')
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product.discounted_price:
            total = self.product.discounted_price * self.quantity
        else:
            total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
