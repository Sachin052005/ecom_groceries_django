from django.contrib import admin
from .models import Cart, Product,Customer,Payment,Orderplaced,ProductImage
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
# Register your models here.
from unfold.admin import ModelAdmin as UnfoldModelAdmin
@admin.register(Product)
class ProductModelAdmin(UnfoldModelAdmin):
    list_display = ['id', 'title', 'discounted_price','category', 'Product_image']
    
@admin.register(Customer)
class CustomerModelAdmin(UnfoldModelAdmin):
    list_display =  ['name', 'locality', 'city', 'mobile', 'zipcod', 'state']

@admin.register(Cart)
class CartModelAdmin(UnfoldModelAdmin):
    list_display =  ['id', 'user', 'product', 'quantity']
    def products(self,obj):
        link =reverse("admin:app_label_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(UnfoldModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(Orderplaced)
class OrderPlacedModelAdmin(UnfoldModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']
    def customer(self,obj):
        link =reverse("admin:app_label_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.title)
    
    def product(self,obj):
        link =reverse("admin:app_label_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    
    def payments(self,obj):
        link =reverse("admin:app_label_payment_change",args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>',link,obj.payment.razorpay_payment)

