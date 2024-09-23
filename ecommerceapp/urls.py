from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('category/', views.categoryView.as_view(),name="category")
]