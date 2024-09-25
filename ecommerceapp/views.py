from django.shortcuts import render
from django.views import View
from .models import Product, CATEGORY_CHOICES  # Add CATEGORY_CHOICES here



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