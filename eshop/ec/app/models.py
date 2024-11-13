from django.db import models
from django.contrib.auth.models import User

#create your models
STATE_CHOICES =(
('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
('Andhra Pradesh','Andhra Pradesh'),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chhattisgarh','Chhattisgarh'),
('Goa','Goa'),
('Gujarat','Gujarat'),
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'),
('Jharkhand','Jharkhand'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'),
('Manipur','Manipur'),
('Meghalaya','Meghalaya'),
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),
('Odisha','Odisha'),
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'),
('Telangana','Telangana'),
('Tripura','Tripura'),
('Uttar Pradesh','Uttar Pradesh'),
('Uttarakhand','Uttarakhand'),
('West Bengal','West Bengal'),

)

# Define category choices
# Define category choices
CATEGORY_CHOICES = (
    ('AR', 'Atta, Rice, Dal'),
    ('OG', 'Oil, Ghee'),
    ('DB', 'Dairy, Bakery'),
    ('PS', 'Pet Supplies'),
    ('SS', 'Spices, Salt, Sugar'),
    ('DF', 'Dry Fruits, Nuts, Seeds'),
    ('CN', 'Biscuits, Chips, Namkeens'),
    ('BE', 'Breakfast Essentials'),
    ('BS', 'Body, Skincare'),
    ('BG', 'Beauty, Grooming'),
    ('OC', 'Oral Care'),
    ('BA', 'Baby Care'),
    ('HW', 'Hygiene, Wellness'),
    ('LD', 'Laundry, Dishwash'),
    ('HC', 'Household, Cleaning'),
    ('HK', 'Home, Kitchen'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()  
    discounted_price = models.FloatField()  
    description = models.TextField(default='')
    composition =models.TextField(default='')
    uses = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    Product_image = models.ImageField(upload_to='products/')
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # For regular image upload
    gif_url = models.URLField(max_length=500, null=True, blank=True)  # For uploading GIF URL

    def __str__(self):
        return self.product.title




class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcod = models.IntegerField()  
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price  
    
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)

STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'), 
        ('Pending', 'Pending'),
    )


class Orderplaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE,default="")  
    admin_notified = models.BooleanField(default=False) 
    canceled_by = models.ForeignKey(User, null=True, blank=True, related_name='canceled_orders', on_delete=models.SET_NULL)
    canceled_date = models.DateTimeField(null=True, blank=True)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price  



class Review(models.Model):
    SENTIMENT_CHOICES = [
        (1, 'Bad ★😡'),
        (2, 'Weak★★😟'),
        (3, 'Neutral★★★😐'),
        (4, 'Good ★★★★😊'),
        (5, 'Excellent ★★★★★😄'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=SENTIMENT_CHOICES)  # Updated for sentiments
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} - {self.get_rating_display()}"
