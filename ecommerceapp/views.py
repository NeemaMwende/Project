from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Customer, Cart, Address, Wishlist, Order, Contact
from .forms import CustomerRegistrationForm, CustomerProfileForm, ContactForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.db import transaction
import stripe
from django.conf import settings
#from user_payment.models import UserPayment
from django.views.decorators.csrf import csrf_exempt
import time

stripe.api_key = settings.STRIPE_SECRET_KEY

# Home View
def home(request):
    products = Product.objects.all()
    return render(request, "app/home.html", {'products': products})

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

# Category View
class CategoryView(View):
    def get(self, request, val):
        products = Product.objects.filter(category=val)
        return render(request, "app/category.html", {'products': products})

class CategoryTitle(View):
    def get(self, request, val):
        products = Product.objects.filter(title=val)
        return render(request, "app/category_title.html", {'products': products})

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
        return render(request, "app/profile.html", {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Saved Successfully")
        return render(request, "app/profile.html", {'form': form})

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add})

class UpdateAddress(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerProfileForm(instance=customer)
        return render(request, 'app/updateAddress.html', {'form': form})

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
        return redirect("app:address")

# Add to Cart
@login_required
def add_to_cart(request):
    user = request.user
    prod_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=prod_id)
    
    try:
        with transaction.atomic():
            cart_item, created = Cart.objects.get_or_create(user=user, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
    except IntegrityError:
        return redirect('error_page')
    
    return redirect('/cart')

# Show Cart View
@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart)
    totalamount = amount + 40  # Shipping fee
    return render(request, 'app/addtocart.html', {'cart': cart, 'amount': amount, 'totalamount': totalamount})

# Increment Quantity
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.quantity += 1
        cart_item.save()
        cart_data = calculate_cart_totals(request.user)
        return JsonResponse(cart_data)

# Decrement Quantity
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        cart_data = calculate_cart_totals(request.user)
        return JsonResponse(cart_data)

# Remove from Cart
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        if cart_item:
            cart_item.delete()
        cart_data = calculate_cart_totals(request.user)
        return JsonResponse(cart_data)

# Calculate Cart Totals
def calculate_cart_totals(user):
    cart = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart)
    totalamount = amount + 40  # Shipping fee
    quantity = cart[0].quantity if cart else 0
    return {'amount': amount, 'totalamount': totalamount, 'quantity': quantity}

# def create_checkout_session(request):
#     user = request.user
#     address_id = request.POST.get('address')
#     custom_address = request.POST.get('customAddress')

#     # Handle address creation or selection
#     if custom_address:
#         address_parts = custom_address.split(',')
#         address_line = address_parts[0].strip()
#         city = address_parts[1].strip() if len(address_parts) > 1 else ''
#         zip_code = address_parts[2].strip() if len(address_parts) > 2 else ''
#         address = Address.objects.create(user=user, address_line=address_line, city=city, zip_code=zip_code)
#     else:
#         address = Address.objects.get(id=address_id)

#     cart_items = Cart.objects.filter(user=user)
#     line_items = []

#     for item in cart_items:
#         line_items.append({
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': item.product.title,
#                 },
#                 'unit_amount': int(item.product.discounted_price * 100),  # Stripe uses cents
#             },
#             'quantity': item.quantity,
#         })

#     YOUR_DOMAIN = 'http://localhost:8000'  # Replace with your domain in production

#     try:
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=line_items,
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         return redirect(checkout_session.url)
#     except Exception as e:
#         return render(request, 'error.html', {'error': str(e)})

# Checkout View
class Checkout(View):
    def get(self, request):
        user = request.user
        addresses = Address.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        totalamount = amount + 40  # Include shipping cost
        return render(request, 'app/checkout.html', {
            'addresses': addresses,
            'cart_items': cart_items,
            'amount': amount,
            'totalamount': totalamount,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,  # Pass the Stripe public key to the template
        })

    def post(self, request):
        user = request.user
        address_id = request.POST.get('address')
        custom_address = request.POST.get('customAddress')
        payment_method_id = request.POST.get('paymentMethodId')  # Get the payment method ID from the request

        # Handle address creation or selection
        if custom_address:
            address_parts = custom_address.split(',')
            address_line = address_parts[0].strip()
            city = address_parts[1].strip() if len(address_parts) > 1 else ''
            zip_code = address_parts[2].strip() if len(address_parts) > 2 else ''
            address = Address.objects.create(user=user, address_line=address_line, city=city, zip_code=zip_code)
        else:
            address = Address.objects.get(id=address_id)

        # Calculate total amount
        cart_items = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        totalamount = amount + 40  # Include shipping cost

        # Create a Stripe payment intent
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(totalamount * 100),  # Amount in cents
                currency='usd',  # Change to your desired currency
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
            )

            # Process successful payment
            for item in cart_items:
                OrderPlaced(user=user, customer=address, product=item.product, quantity=item.quantity).save()
                item.delete()

            messages.success(request, "Your order has been placed successfully!")
            return redirect("app:home")

        except stripe.error.CardError as e:
            # Handle card error
            messages.error(request, "There was an error processing your payment.")
            return redirect("app:checkout")

        except Exception as e:
            messages.error(request, str(e))
            return redirect("app:checkout")

def create_payment_intent(request):
    if request.method == 'POST':
        # Create a PaymentIntent with Stripe
        amount = int(request.POST.get('amount'))  # Convert to integer for Stripe
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount * 100,  # Convert amount to cents for Stripe
                currency='usd',
                automatic_payment_methods={'enabled': True},
            )
            return JsonResponse({'clientSecret': intent['client_secret']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)

def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        # Convert query to lowercase and perform a case-insensitive search based on title and description
        query = query.lower()
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'app/product_search_results.html', {'products': products, 'query': query})

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'orders': orders})

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})

# views.py (with model saving)
from .models import Contact

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save data to the database
            contact = Contact(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            contact.save()

            messages.success(request, "Your message has been sent successfully!")
            return redirect('app:contact')
        else:
            messages.error(request, "There was an error sending your message. Please try again.")
    else:
        form = ContactForm()

    return render(request, 'app/contact.html', {'form': form})

    
def thank_you(request):
    return render(request, 'app/thank_you.html')

#Checkout session creation view
# def create_checkout_session(request):
#     YOUR_DOMAIN = 'http://localhost:8000'  # Replace with your domain

#     try:
#         # Create a new Stripe Checkout Session
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'usd',
#                         'product_data': {
#                             'name': 'Cool Product',
#                         },
#                         'unit_amount': 2000,  # 2000 cents = $20
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         return redirect(checkout_session.url)
#     except Exception as e:
#         return render(request, 'error.html', {'error': str(e)})

# Success page view
def success(request):
    return render(request, 'success.html')

# Cancel page view
def cancel(request):
    return render(request, 'cancel.html')
