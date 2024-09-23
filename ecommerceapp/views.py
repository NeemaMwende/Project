from django.shortcuts import render
from django.http import HttpResponse
from urllib import request
from django.views import View

# Create your views here.
def home(request):
    return render(request, "app/home.html")

class categoryView(View):
    def get(self, request, val):
        return render(request, "app/category.html",locals())