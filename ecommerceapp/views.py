from django.shortcuts import render, redirect
from django.views import View
from .models import Product, CATEGORY_CHOICES, Customer  # Add CATEGORY_CHOICES here
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from .forms import LoginForm

def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self, request, val):
        products = Product.objects.filter(category=val)
        categories = dict(CATEGORY_CHOICES)
        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, "app/category.html", context)

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title').annotate(total=Count(''))
        return render(request, "app/category_title.html", context)

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        context = {
            'product': product,
        }
        return render(request, "app/product_detail.html", context)

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {
            'form': form
        }
        return render(request, "app/customerregistration.html", context)

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
            return render(request, "app/customerregistration.html", {'form': CustomerRegistrationForm()})
        else:
            messages.warning(request, "Invalid Input Data")
            context = {
                'form': form
            }
            return render(request, "app/customerregistration.html", context)

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "app/profile.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save() 
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app/profile.html", locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    context = {'add': add}
    return render(request, 'app/address.html', context)

class UpdateAddress(View):
    def get(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=customer)
        context = {
            'form': form,
            'customer': customer
        }
        return render(request, 'app/updateAddress.html', context)

    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("app:address")
