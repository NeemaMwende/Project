from django.shortcuts import render
from django.views import View
from .models import Product, CATEGORY_CHOICES  # Add CATEGORY_CHOICES here



def home(request):
    return render(request, "app/home.html")

class CategoryView(View):
    def get(self, request, val):
        products = Product.objects.filter(category=val)
        categories = dict(CATEGORY_CHOICES)  # Now this should work
        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, "app/category.html", context)