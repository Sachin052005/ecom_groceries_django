from django.urls import path
from . import views
from  django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordResetForm, MypasswordChangeForm,MySetPasswordForm
from .views import (
    product_list, product_create, product_update, product_delete,
    customer_list, customer_create, customer_update, customer_delete,cart_list, cart_add, cart_edit,cart_delete,
    order_list, order_add, order_edit,order_delete,
    payment_list, payment_add, payment_edit,payment_delete,dashboard
)

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('product-detail/<int:pk>/',views.ProductDetail.as_view(), name='product-detail'),
# Login redirect path
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('categoryzz-title/<val>/', views.CategoryTitle.as_view(), name='category-title'),

# Update address
    path('updateAddress/<int:pk>/', views.updateAddress.as_view(), name='updateAddress'),

# Registration
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

# Login process
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('delete_address/<int:pk>/',views.delete_address, name='deleteAddress'),
    path('logout/',views.Logout, name="logout"),
# Password reset & forgetpassword
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/passwordreset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordresetconfirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordresetcomplete.html'),name='password_reset_complete'),
 
#add to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('delivered_orders/', views.delivered_orders, name='delivered_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
#search
    path('search/',views.search,name='search'),
#invoice
    path('download_invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('generate_qr/<int:order_id>/', views.generate_qr, name='generate_qr'),

    
#admin
    path('products/', product_list, name='product_list'),
    path('products/create/', product_create, name='product_create'),
    path('products/update/<int:pk>/', product_update, name='product_update'),
    path('products/delete/<int:pk>/', product_delete, name='product_delete'),
    
    path('customers/', customer_list, name='customer_list'),
    path('customers/create/', customer_create, name='customer_create'),
    path('customers/update/<int:pk>/', customer_update, name='customer_update'),
    path('customers/delete/<int:pk>/', customer_delete, name='customer_delete'),

    path('carts/', cart_list, name='cart_list'),
    path('carts/add/', cart_add, name='cart_add'),
    path('carts/edit/<int:pk>/', cart_edit, name='cart_edit'),
    path('carts/delete/<int:pk>/', cart_delete, name='cart_delete'),

    path('order/', order_list, name='order_list'),
    path('orders/add/', order_add, name='order_add'),
    path('orders/edit/<int:pk>/', order_edit, name='order_edit'),
    path('orders/delete/<int:pk>/', order_delete, name='order_delete'),

    path('payments/', payment_list, name='payment_list'),
    path('payments/add/', payment_add, name='payment_add'),
    path('payments/edit/<int:pk>/', payment_edit, name='payment_edit'),
    path('payments/delete/<int:pk>/', payment_delete, name='payment_delete'), 

    path('dashboard/', dashboard, name='dashboard'),
#logout
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),


# Password change
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MypasswordChangeForm,success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),



    path('upload/', views.upload_and_match_product, name='upload_and_match_product'),
   




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header='Grocery Shop'
admin.site.site_title='Grocery Shop'
admin.site.site_index_title='Welcome to Grocery Shop'