from django.shortcuts import render
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
        categories = dict(CATEGORY_CHOICES)  # Now this should work
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
            'form': form  # Ensure 'form' is passed to the template
        }
        return render(request, "app/customerregistration.html", context)

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)  # Create the form with POST data
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
            return render(request, "app/customerregistration.html", {'form': CustomerRegistrationForm()})  # Reset form on success
        else:
            messages.warning(request, "Invalid Input Data")
            context = {
                'form': form  # Pass the invalid form back to the template
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
