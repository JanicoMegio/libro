from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
    path('login', views.login_user, name="login"),
    path('register', views.register_user, name="register"),
    path('logout', views.logout_user, name="logout"),
    
    path('account', views.user_account, name="user-account"),
    path('update-info/<int:pk>', views.update_user_info, name="update-info"),
    path('user-info', views.user_info, name="user-info"),

    path('store-page/', views.store_page, name='store-page'),
    path('book-detail/<int:pk>', views.book_detail, name="book-detail"),
    path('new-book', views.new_books, name="new-books"),

    path('cart-notification', views.cart_notification, name="cart-notification"),
    
    
    path('add-to-cart/<int:pk>', views.add_to_cart, name="add-to-cart"),
    path('cart', views.view_cart, name="view-cart"),


    path('delete-item/<int:pk>', views.delete_item_cart, name="delete-item"),
    path('minus-item/<int:pk>', views.minus_quantity, name="minus-item"),
    path('plus-item/<int:pk>', views.plus_quantity, name="plus-item"),
    
    path('checkout', views.checkout_item, name="checkout-item"),
    path('payment-success', views.payment_success, name='payment-success'),
    path('order', views.user_order, name="order"),
    path('order-received/<int:pk>', views.item_received, name="order-received"),
    path('order-history', views.order_history, name="order-history"),


    path('create-review/<int:pk>', views.create_review, name="create-review"),
    
    #path('create-checkout', views.create_checkout_session, name="create-checkout"),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
