from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import OrderForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required


from django.http import JsonResponse
import json
import datetime

from .utils import cookieCart, cartData, guestOrder

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def home(request):

    return render(request, 'store/home.html', {})

# REGISTER FORM PAGE


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')

    context = {'form': form}
    return render(request, 'store/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'username OR password is incorrect')

        context = {}
        return render(request, "store/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def store(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    try:
        data = cartData(request)
    except User.customer.RelatedObjectDoesNotExist:
        # handle the case when customer does not exist
        # for example, create the customer object
        customer = Customer.objects.create(
            user=request.user, name=request.user.username, email=request.user.email)
        data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    total_product_price = 0
    for item in items:
        if request.user.is_authenticated:
            product_price_quantity = item.product.price * item.quantity
            total_product_price = total_product_price + product_price_quantity
        else:
            product_price_quantity = item["product"]["price"] * item["quantity"]
            total_product_price = total_product_price + product_price_quantity
    print(total_product_price)

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'total_product_price':total_product_price}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    # print('asuiduiwdhu')
    # print(cartItems)
    # print(order)
    # print(items)

    total_product_price = 0
    print(items)
    print('items')
    for item in items:
        # print(item.product.price)
        # print(item.quantity)
        # print(item["product"])
        # print(type(item))
        if request.user.is_authenticated:
            product_price_quantity = item.product.price * item.quantity
            total_product_price = total_product_price + product_price_quantity
        else:
            product_price_quantity = item["product"]["price"] * item["quantity"]
            total_product_price = total_product_price + product_price_quantity
    print(total_product_price)

    # delivery_charge = 10

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'total_product_price':total_product_price}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    # Update the order total to include delivery cost and discount
    order.delivery_cost = float(data['form']['deliveryCost'])
    order.discount_amount = float(data['form']['discountAmount'])
    order.total_price = total + order.delivery_cost - order.discount_amount

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)


# original start
# def processOrder(request):
#     transaction_id = datetime.datetime.now().timestamp()
#     data = json.loads(request.body)

#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(
#             customer=customer, complete=False)
#     else:
#         customer, order = guestOrder(request, data)

#     total = float(data['form']['total'])
#     order.transaction_id = transaction_id

#     if total == float(order.get_cart_total):
#         order.complete = True
#     order.save()

#     if order.shipping == True:
#         ShippingAddress.objects.create(
#             customer=customer,
#             order=order,
#             address=data['shipping']['address'],
#             city=data['shipping']['city'],
#             state=data['shipping']['state'],
#             zipcode=data['shipping']['zipcode'],
#         )

#     return JsonResponse('Payment submitted..', safe=False)
# original end
