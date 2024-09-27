from django.shortcuts import render, redirect ,get_object_or_404
from django.views import View
from .models import Product, Customer, Cart, Address
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.db import transaction

# Home View
def home(request):
    products = Product.objects.all()
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

# Category View
class CategoryView(View):
    def get(self, request, val):
        products = Product.objects.filter(category=val)
        context = {
            'products': products,
        }
        return render(request, "app/category.html", context)

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        return render(request, "app/category_title.html", {'product': product})

# Product Detail View
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/product_detail.html", {'product': product})

# Customer Registration
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Registered Successfully")
        return render(request, "app/customerregistration.html", {'form': form})

# Profile View
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "app/profile.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            form.save(user=user)
            messages.success(request, "Profile Saved Successfully")
        return render(request, "app/profile.html", locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add})

class UpdateAddress(View):
    def get(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=customer)
        return render(request, 'app/updateAddress.html', {'form': form})

    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
        return redirect("app:address")

# Add to Cart View
@login_required
def add_to_cart(request):
    user = request.user
    prod_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=prod_id)
    
    try:
        # Use atomic transaction to avoid race conditions
        with transaction.atomic():
            # Check if product is already in the user's cart
            cart_item, created = Cart.objects.get_or_create(user=user, product=product)
            
            if not created:
                # If the item already exists, increment the quantity
                cart_item.quantity += 1
                cart_item.save()
    
    except IntegrityError:
        # Handle any unexpected integrity errors
        return redirect('error_page')  # Redirect to an error page or display a message
    
    return redirect('/cart')# Show Cart View
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart)
    totalamount = amount + 40  # Adding shipping charge
    return render(request, 'app/addtocart.html', locals())

# Increment Quantity (Plus Cart)
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.quantity += 1
        cart_item.save()
        cart_data = calculate_cart_totals(request.user)
        return JsonResponse(cart_data)

# Decrement Quantity (Minus Cart)
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        cart_data = calculate_cart_totals(request.user)
        return JsonResponse(cart_data)

# Remove Item from Cart
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        # Fetch the first matching cart item
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        
        if cart_item:  # Check if the cart_item exists
            cart_item.delete()
        
        cart_data = calculate_cart_totals(request.user)
        return JsonResponse(cart_data)

# Calculate Cart Totals
def calculate_cart_totals(user):
    cart = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart)
    totalamount = amount + 40  # Adding shipping charge
    quantity = cart[0].quantity if cart else 0
    return {'amount': amount, 'totalamount': totalamount, 'quantity': quantity}

class Checkout(View):
    def get(self, request):
        user = request.user
        addresses = Address.objects.filter(user=user)  # Fetch user's addresses
        cart_items = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        totalamount = amount + 40  # Adding shipping charge
        return render(request, 'app/checkout.html', {'addresses': addresses, 'cart_items': cart_items, 'amount': amount, 'totalamount': totalamount})

    def post(self, request):
        user = request.user
        address_id = request.POST.get('address')
        custom_address = request.POST.get('customAddress')
        
        # Check if a custom address was provided
        if custom_address:
            # Split the custom address into components
            address_parts = custom_address.split(',')
            address_line = address_parts[0].strip()
            city = address_parts[1].strip() if len(address_parts) > 1 else ''
            zip_code = address_parts[2].strip() if len(address_parts) > 2 else ''
            
            # Create a new address for the user
            address = Address.objects.create(user=user, address_line=address_line, city=city, zip_code=zip_code)
        else:
            # Get the selected address from the dropdown
            address = Address.objects.get(id=address_id)
        
        # Process the order
        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            OrderPlaced(user=user, customer=address, product=item.product, quantity=item.quantity).save()
            item.delete()  # Clear cart after order
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect("app:home")