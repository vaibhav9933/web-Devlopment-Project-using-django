from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Cart, Customer, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django .http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        totaliteam = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totaliteam = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/home.html', {
            'topwears': topwears,
            'bottomwears': bottomwears,
            'mobiles': mobiles, 'totaliteam': totaliteam})


class ProductDetailView(View):
    def get(self, request, pk):
        totaliteam = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart =False
        if request.user.is_authenticated:
            totaliteam = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totaliteam': totaliteam})


@login_required()
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required()
def show_cart(request):
    totaliteam = 0
    global totalamount
    if request.user.is_authenticated:
        totaliteam = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount, 'totaliteam':totaliteam})
        else:
            return render(request,'app/emptycart.html')



def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
          tempamount = (p.quantity * p.product.discounted_price)
          amount += tempamount

        data = {
          'quantity': c.quantity,
          'amount': amount,
          'totalamount': amount + shipping_amount
          }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
          tempamount = (p.quantity * p.product.discounted_price)
          amount += tempamount

        data = {
          'quantity': c.quantity,
          'amount': amount,
          'totalamount': amount + shipping_amount
          }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
          tempamount = (p.quantity * p.product.discounted_price)
          amount += tempamount

        data = {
          'amount': amount,
          'totalamount': amount + shipping_amount
          }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required()
def address(request):
    totaliteam = 0
    if request.user.is_authenticated:
        totaliteam = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary','totaliteam': totaliteam})


@login_required()
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


def mobile(request, data=None):
    totaliteam = 0
    global mobiles
    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'vivo' or data == 'poco':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    if request.user.is_authenticated:
        totaliteam = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/mobile.html', {'mobiles': mobiles,'totaliteam': totaliteam})


def topwear(request, data=None):
    totaliteam = 0
    global topwears
    if data is None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'harpa' or data == 'tokyo':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totaliteam = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/topwear.html', {'topwears': topwears,'totaliteam': totaliteam})


def bottomwear(request, data=None):
    totaliteam = 0
    global bottomwears
    if data is None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'kotta' or data == 'samer':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=500)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=1000)
    if request.user.is_authenticated:
        totaliteam = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears,'totaliteam': totaliteam})


def laptop(request, data=None):
    totaliteam = 0
    global laptops
    if data is None:
        laptops = Product.objects.filter(category='L')
    elif data == 'asus' or data == 'hp':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=50000)
    if request.user.is_authenticated:
        totaliteam = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/laptop.html', {'laptops': laptops, 'totaliteam': totaliteam})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required()
def checkout(request):
    totaliteam = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items =Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    if request.user.is_authenticated:
        totaliteam = len(Cart.objects.filter(user=request.user))
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items, 'totaliteam': totaliteam})


@login_required()
def payment_done(request):
    user = request.user
    custid =request.GET.get('custid')
    customer =Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
      OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
      c.delete()
    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    totaliteam = 0
    def get(self, request):
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totaliteam = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        totaliteam = 0
        form = CustomerProfileForm(request.POST)
        if request.user.is_authenticated:
            totaliteam = len(Cart.objects.filter(user=request.user))
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation!! Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totaliteam': totaliteam})

