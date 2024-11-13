from django.db.models import Count 
from django.shortcuts import render,redirect, get_object_or_404
from django.views import View 
from .models import Product,ProductImage,Customer,Cart,Payment,Orderplaced
from .forms import LoginForm,CustomerRegistrationForm,CustomerProfileForm,ProductForm, CustomerForm, CartForm, PaymentForm, OrderplacedForm, ProductImageForm, ProductImageFormSet
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView
import string
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.db.models.functions import TruncDate

#invoice
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from xhtml2pdf import pisa  # Use this to generate PDF

# Create your views here.
class CustomLoginView(auth_views.LoginView):
    template_name = 'app/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        # Redirect superusers to the dashboard
        if self.request.user.is_superuser:
            return reverse_lazy('dashboard')  
   
        elif self.request.user.is_staff:
            return reverse_lazy('home') 
 
        return reverse_lazy('home')

def Logout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('home') 

@login_required
def home(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        products = Product.objects.all()
    return render(request, "app/home.html",locals())


class CategoryView(View):  
    def get(self, request, val):
        totalitem=0
        if request.user.is_authenticated:
              totalitem=len(Cart.objects.filter(user=request.user))
        # Filter products based on the category slug
        products = Product.objects.filter(category=val)
        # Pass products to the template as context
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/Category.html",locals()) 

from .forms import ReviewForm
from django.db.models import Avg
class ProductDetail(View):
    def get(self, request, pk):
        # Fetch the current product by its primary key
        product = get_object_or_404(Product, pk=pk)
        
        # Fetch related products and images
        related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)
        product_images = ProductImage.objects.filter(product=product)
        
        # Calculate total items in the cart for authenticated users
        totalitem = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
        
        # Fetch reviews and average rating
        reviews = product.reviews.all()
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Filter reviews by rating
        reviews_by_rating = {
            '5_star': reviews.filter(rating=5),
            '4_star': reviews.filter(rating=4),
            '3_star': reviews.filter(rating=3),
            '2_star': reviews.filter(rating=2),
            '1_star': reviews.filter(rating=1),
        }
        
        review_form = ReviewForm()

        # Render the template with all context data
        context = {
            'product': product,
            'product_images': product_images,
            'totalitem': totalitem,
            'related_products': related_products,
            'avg_rating': avg_rating,
            'reviews_by_rating': reviews_by_rating,
            'review_form': review_form,
        }
        return render(request, "app/productdetail.html", context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        review_form = ReviewForm(request.POST, request.FILES)  # Include request.FILES for image uploads

        totalitem = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product-detail', pk=product.pk)

        # Re-fetch data for invalid form submission
        related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)
        product_images = ProductImage.objects.filter(product=product)
        reviews = product.reviews.all()
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Filter reviews by rating
        reviews_by_rating = {
            '5_star': reviews.filter(rating=5),
            '4_star': reviews.filter(rating=4),
            '3_star': reviews.filter(rating=3),
            '2_star': reviews.filter(rating=2),
            '1_star': reviews.filter(rating=1),
        }

        context = {
            'product': product,
            'product_images': product_images,
            'totalitem': totalitem,
            'related_products': related_products,
            'avg_rating': avg_rating,
            'reviews_by_rating': reviews_by_rating,
            'review_form': review_form,
        }
        return render(request, "app/productdetail.html", context)


class CategoryTitle(View):
    def get(self,request,val):
        products = Product.objects.filter(title=val)
        title = Product.objects.filter(category=products[0].category).values('title')
        totalitem=0
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user)) 
        return render(request,"app/Category.html",locals()) 

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully.")
        else:
            messages.warning(request, "Invalid input data.")
        return render(request, 'app/customerregistration.html', locals())

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem=0
        if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html',locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcod']

            # Always create a new Customer instance
            Customer.objects.create(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                zipcod=zipcode,
            )
            messages.success(request, "New address saved successfully.")
            return redirect('address')  
            
        else:
            messages.warning(request, "Invalid input data.")
        
        return render(request, 'app/profile.html',locals()) 

# to view the address filter user name 
def address(request):
    add =Customer.objects.filter(user=request.user)
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html',locals()) 


def delete_address(request, pk):
    Customer.objects.filter(pk=pk, user=request.user).delete()  # Deletes the address if it exists for the user
    messages.success(request, "Address deleted successfully.")
    return redirect('address')

#update address
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem=0
        if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals()) 

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            # Corrected 'Cleaned_data' to 'cleaned_data'
            add.name = form.cleaned_data['name']  
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcod = form.cleaned_data['zipcod']
            add.save()
            messages.success(request, 'Congratulations! Profile Updated Successfully')
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('address')



def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id) 
    Cart(user=user, product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0

    # Calculate the total amount for the items in the cart
    for p in cart:
        value= p.quantity * p.product.discounted_price
        amount = amount+value
        totalamount=amount+40
        totalitem=0
        if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals())  

class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        totalitem=0
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
        famount = 0
        
        for p in cart_items:
            value = p.quantity * p.product.discounted_price  # Accessing discounted_price from the product
            famount += value
            
        totalamount = famount + 40 
        razoramount = int(totalamount * 100) 
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount,"currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)

        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status

            )
            payment.save()
        return render(request, 'app/checkout.html', locals())
    

from django.core.mail import send_mail

from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id', 'dummy_order_id')  # Use dummy ID for testing
    payment_id = request.GET.get('payment_id', 'dummy_payment_id')  # Use dummy payment ID for testing
    cust_id = request.GET.get('cust_id')
    user = request.user

    # Retrieve the customer based on cust_id
    customer = get_object_or_404(Customer, id=cust_id)

    # Try to retrieve the existing payment or create one if it doesn't exist
    payment, created = Payment.objects.get_or_create(
        razorpay_order_id=order_id,
        defaults={
            'user': user,
            'amount': request.POST.get('totalamount', 0),
            'razorpay_payment_id': payment_id,
            'paid': True
        }
    )

    # If the payment already exists but is not marked as paid, update it
    if not created:
        payment.razorpay_payment_id = payment_id
        payment.paid = True
        payment.save()

    # Process cart items to place orders and then clear the cart
    cart_items = Cart.objects.filter(user=user)
    product_details = ""  # Initialize a string to store product details for the email
    total_amount = 0  # Initialize total amount

    for item in cart_items:
        product_details += f"\n- {item.product.title}: {item.quantity} x Rs. {item.product.discounted_price}"
        total_amount += item.quantity * item.product.discounted_price

        # Place the order for each item
        Orderplaced.objects.create(
            user=user,
            customer=customer,
            product=item.product,
            quantity=item.quantity,
            payment=payment,
            status="Pending"
        )
        item.delete()  # Remove item from cart after placing the order

    # Construct email content for order confirmation with product details
    user_email = user.email
    subject = 'Order Confirmation'
    message = (
        f"Dear {user.username},\n\n"
        f"Your order with Order ID {order_id} has been placed successfully! Here are the details:\n\n"
        f"Products Ordered:\n{product_details}\n\n"
        f"Total Amount: Rs. {total_amount}\n"
        f"Thank you for shopping with us!\n\nBest regards,\neshop"
    )
    email_from = 'idpsachin@gmail.com'
    recipient_list = [user_email]

    # Send the order confirmation email
    send_mail(subject, message, email_from, recipient_list)

    # Redirect to the orders page after processing and email sending
    return redirect('orders')



   
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()  
        # Exclude delivered and cancelled orders from the orders page
        order_placed = Orderplaced.objects.filter(user=request.user).exclude(status__in=['Delivered', 'Cancelled']) 
    return render(request, 'app/orders.html', locals())


def delivered_orders(request): 
    delivered_orders = Orderplaced.objects.filter(user=request.user, status__in=['Delivered', 'Cancelled'])
    return render(request, 'app/delivered_orders.html', {'delivered_orders': delivered_orders})


def cancel_order(request, order_id):
    # Try to retrieve the order; if it doesn't exist, do not raise a 404 error.
    try:
        order = Orderplaced.objects.get(id=order_id)
    except Orderplaced.DoesNotExist:
        # Order does not exist; redirect or handle accordingly
        return redirect('orders')  # Redirecting back to orders if the order doesn't exist

    # Only allow cancellation if the order is not already delivered or canceled
    if order.status != 'Delivered' and order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.save()

    return redirect('orders')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.quantity += 1
            c.save()  

            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40  

            # Debugging logs
            print(f"Amount: {amount}, Total Amount: {totalamount}")

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.quantity -= 1
            c.save()  

            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40  

            # Debugging logs
            print(f"Amount: {amount}, Total Amount: {totalamount}")

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.delete()  

            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40  # Add shipping cost

            # Debugging logs
            print(f"Amount: {amount}, Total Amount: {totalamount}")

            data = {
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse(data)
            



def search(request):
    query = request.GET.get('search', '').strip()  # Strip whitespace
    query = query.rstrip(string.punctuation)  # Remove trailing punctuation

    totalitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    # Log the cleaned query
    print(f"Search query: '{query}'")

    # Perform the search on the title field of the Product model
    products = Product.objects.filter(Q(title__icontains=query))

    # Log the number of products found
    print(f"Number of products found: {len(products)}")

    return render(request, 'app/search.html', {
        'products': products,
        'totalitem': totalitem,
        'query': query,
        'message': "No products found matching your search criteria." if not products else ""
    })


from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models import Orderplaced  # Make sure to import your model

def download_invoice(request, order_id):
    try:
        order = Orderplaced.objects.get(id=order_id, user=request.user, status="Delivered")
    except Orderplaced.DoesNotExist:
        raise Http404("Order not found or not delivered.")
    
    # Generate the PDF using a template
    template_path = 'app/invoice_template.html'
    context = {'order': order}
    
    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()
    template = get_template(template_path)
    html = template.render(context)
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=buffer)
    buffer.seek(0)  # Move to the beginning of the buffer

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    # Create the email
    email = EmailMessage(
        subject='Your Invoice',
        body='Please find your invoice attached.',
        from_email='idpsachin@example.com',  # Replace with your email
        to=[request.user.email],
    )
    email.attach(f'invoice_{order.id}.pdf', buffer.getvalue(), 'application/pdf')
    email.send()

    # Return the PDF response to the user
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{order.id}.pdf"'  # Display in browser
    return response

import qrcode

def generate_qr(request, order_id):
    try:
        order = Orderplaced.objects.get(id=order_id, user=request.user, status="Delivered")
        qr_url = request.build_absolute_uri(f'/download_invoice/{order.id}/')
        
        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        return HttpResponse(buffer, content_type="image/png")
    except Orderplaced.DoesNotExist:
        raise Http404("Order not found or not delivered.")


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        # Debug: print email information
        print(f"Sending email to: {form.cleaned_data.get('email')}")
        print(f"From: {settings.EMAIL_HOST_USER}")
        return super().form_valid(form)

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.utils.translation import gettext as _

class CustomPasswordResetView(PasswordResetView):
    template_name = 'app/password_reset_form.html'
    email_template_name = 'app/password_reset_email.html'
    success_url = '/password-reset/done/'  # Adjust to your success URL
    from_email = 'your_email@example.com'  # Change to your sender email

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'app/password_reset_confirm.html'

    def form_valid(self, form):
        messages.success(self.request, _("Your password has been set. You may go ahead and log in now."))
        return super().form_valid(form)


# Product views
def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage
from .forms import ProductForm, ProductImageFormSet

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            images = formset.save(commit=False)
            for image in images:
                image.product = product  # Set the foreign key to the product
                image.save()
            return redirect('product_list')
    else:
        form = ProductForm()
        formset = ProductImageFormSet(queryset=ProductImage.objects.none())  # Initialize with no images

    return render(request, 'admin/product_form.html', {'form': form, 'image_formset': formset})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)  # Link to the existing product
        if form.is_valid() and formset.is_valid():
            form.save()
            images = formset.save(commit=False)
            for image in images:
                image.product = product
                image.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)  # Populate with existing images

    return render(request, 'admin/product_form.html', {'form': form, 'image_formset': formset})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

# Customer views
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'admin/customer_list.html', {'customers': customers})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'admin/customer_form.html', {'form': form})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'admin/customer_form.html', {'form': form})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('customer_list')

# Cart Views
def cart_list(request):
    carts = Cart.objects.all()
    return render(request, 'admin/cart_list.html', {'carts': carts})

def cart_add(request):
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cart_list')
    else:
        form = CartForm()
    return render(request, 'admin/cart_management.html', {'form': form})

def cart_edit(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    if request.method == 'POST':
        form = CartForm(request.POST, instance=cart)
        if form.is_valid():
            form.save()
            return redirect('cart_list')
    else:
        form = CartForm(instance=cart)
    return render(request, 'admin/cart_management.html', {'form': form})

def cart_delete(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    cart.delete()
    return redirect('cart_list')  # Redirect back to the cart list

# Order Placed Views
def order_list(request):
    orders = Orderplaced.objects.all()
    return render(request, 'admin/order_list.html', {'orders': orders})

def order_add(request):
    if request.method == 'POST':
        form = OrderplacedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderplacedForm()
    return render(request, 'admin/order_management.html', {'form': form})

def order_edit(request, pk):
    order = get_object_or_404(Orderplaced, pk=pk)
    if request.method == 'POST':
        form = OrderplacedForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderplacedForm(instance=order)
    return render(request, 'admin/order_management.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(order, pk=pk)
    order.delete()
    return redirect('order_list')  # Redirect back to the order list

# Payment Views
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'admin/payment_list.html', {'payments': payments})

def payment_add(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'admin/payment_management.html', {'form': form})

def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'admin/payment_management.html', {'form': form})

def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    payment.delete()
    return redirect('payment_list')  # Redirect back to the payment list

from django.db.models import F

def dashboard(request):
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_orders = Orderplaced.objects.count()
    total_cart_items = Cart.objects.count()
    total_payment_items = Payment.objects.count()
    
    # Aggregate orders by date
    order_counts_by_date = (
        Orderplaced.objects.annotate(order_date=TruncDate('ordered_date'))
        .values('order_date')
        .annotate(count=Count('id'))
        .order_by('order_date')
    )
    
    # Separate data into labels (dates) and counts
    dates = [order['order_date'].strftime('%Y-%m-%d') for order in order_counts_by_date]
    counts = [order['count'] for order in order_counts_by_date]

    # Get product data for price chart
    products = Product.objects.values('title', 'selling_price', 'discounted_price')
    product_names = [product['title'] for product in products]
    selling_prices = [product['selling_price'] for product in products]
    discounted_prices = [product['discounted_price'] for product in products]

    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_cart_items': total_cart_items,
        'total_payment_items': total_payment_items,
        'dates': dates,
        'counts': counts,
        'product_names': product_names,
        'selling_prices': selling_prices,
        'discounted_prices': discounted_prices,
    }
    
    return render(request, 'admin/dashboard.html', context)

# import os
# import numpy as np
# import cv2
# from PIL import Image
# from tensorflow.keras.applications import MobileNetV2
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras.models import Model
# from sklearn.metrics.pairwise import cosine_similarity
# from django.shortcuts import render
# from django.conf import settings

# # Load MobileNetV2 model without the top layer for feature extraction
# base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
# model = Model(inputs=base_model.input, outputs=base_model.output)

# def extract_features(image_path):
#     image = Image.open(image_path).convert('RGB')  # Ensure image is in RGB format
#     image = image.resize((224, 224))
#     image_array = np.array(image)
#     image_array = np.expand_dims(image_array, axis=0)
#     image_array = preprocess_input(image_array)
#     features = model.predict(image_array)
#     return features.flatten()


# # Function to find the best-matching product image
# def find_matching_product(uploaded_image_path):
#     uploaded_image = cv2.imread(uploaded_image_path)
#     uploaded_image = cv2.resize(uploaded_image, (224, 224))
#     uploaded_image_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY) 

#     best_match = None
#     lowest_diff = float('inf')

#     # Iterate over all product images in the media folder
#     products = Product.objects.all()
#     for product in products:
#         product_image_path = product.Product_image.path
#         product_image = cv2.imread(product_image_path)
#         product_image = cv2.resize(product_image, (224, 224))
#         product_image_gray = cv2.cvtColor(product_image, cv2.COLOR_BGR2GRAY)

#         # Calculate the difference using Mean Squared Error (MSE)
#         diff = np.mean((uploaded_image_gray - product_image_gray) ** 2)

#         if diff < lowest_diff:
#             lowest_diff = diff
#             best_match = product

#     return best_match

# def upload_and_match_product(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image = request.FILES['image']
#         temp_image_path = 'temp_image.jpg'

#         # Save the uploaded image temporarily for processing
#         with open(temp_image_path, 'wb') as f:
#             for chunk in image.chunks():
#                 f.write(chunk)

#         # Find the matching product
#         matched_product = find_matching_product(temp_image_path)

#         # Remove the temporary image file
#         os.remove(temp_image_path)

#         return render(request, 'app/match_result.html', {'product': matched_product})

#     return render(request, 'app/upload.html')

import os
import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model
from django.shortcuts import render
from .models import Product  # Ensure you import your Product model
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity 

# Load MobileNetV2 model without the top layer for feature extraction
base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)

def extract_features(image_path):
    """Extract features from an image using MobileNetV2."""
    image = Image.open(image_path).convert('RGB')  # Ensure image is in RGB format
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)
    features = model.predict(image_array)
    return features.flatten()

def find_matching_product(uploaded_image_path):
    """Find the product that best matches the uploaded image."""
    # Extract features from the uploaded image
    uploaded_features = extract_features(uploaded_image_path)

    best_match = None
    highest_similarity = -1  # Initialize to a very low value

    # Iterate over all product images in the database
    products = Product.objects.all()
    for product in products:
        product_image_path = product.Product_image.path
        
        # Extract features from the product image
        product_features = extract_features(product_image_path)
        
        # Calculate cosine similarity
        similarity = cosine_similarity([uploaded_features], [product_features])[0][0]

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = product

    return best_match

def upload_and_match_product(request):
    """Handle image upload and find the matching product."""
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg')  # Save to media folder

        # Save the uploaded image temporarily for processing
        with open(temp_image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Find the matching product
        matched_product = find_matching_product(temp_image_path)

        # Remove the temporary image file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

        return render(request, 'app/match_result.html', {'product': matched_product})

    return render(request, 'app/upload.html')