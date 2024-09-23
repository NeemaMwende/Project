from django.contrib import admin
from . models import Product

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']
    # prepopulated_fields = {'slug': ('name',)}
    # list_filter = ('category', 'is_available')
    # list_editable = ('is_available',)