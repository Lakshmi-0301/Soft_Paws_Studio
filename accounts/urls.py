from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path('products/<str:category>/', views.product_list, name='product_list'),
    path('shop_now/',views.contents,name='contents'),
    path('product_detail/<int:product_id>/', views.myproduct, name='myproduct'),
    path("cart/", views.view_cart, name="view_cart"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('cart/data/', views.cart_data, name='cart_data'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/", views.payment_view, name="payment"), 
    path("confirmation/", views.order_confirmation, name="confirmation"),  
    path('order_history/', views.order_history, name='order_history'),
    path("submit_review/", views.submit_review, name="submit_reviews"),
    path("home/", views.home, name="home")

]
