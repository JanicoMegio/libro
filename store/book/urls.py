from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    path('sales', views.sale_dashboard, name="sales"),
    path('item-status/<int:pk>', views.item_status, name="item-status"),
    path('item-status-ofd/<int:pk>', views.item_status_ofd, name="item-status-ofd"),
    
    path('login', views.login_user, name="login"),
    path('register', views.register_user, name="register"),
    path('logout', views.logout_user, name="logout"),
    
    path('account', views.user_account, name="user-account"),
    path('update-info/<int:pk>', views.update_user_info, name="update-info"),
    path('user-info', views.user_info, name="user-info"),

    path('', views.store_page, name='store-page'),
    path('book-detail/<int:pk>', views.book_detail, name="book-detail"),
    path('new-book', views.new_books, name="new-books"),
    path('wishlist', views.wish_list, name="wishlist"),

    path('cart-notification', views.cart_notification, name="cart-notification"),
    
    
    path('add-to-cart/<int:pk>', views.add_to_cart, name="add-to-cart"),
    path('add-to-wishlist/<int:pk>', views.add_to_wishlist, name="add-to-wishlist"),
    path('add-to-cart-wishlist/<int:pk>', views.add_to_cart_wishlist, name="add-to-cart-wishlist"),
    path('cart', views.view_cart, name="view-cart"),

    path('wishlist-item-remove/<int:pk>', views.wishlist_item_remove, name="wishlist-item-remove"),
    path('delete-item/<int:pk>', views.delete_item_cart, name="delete-item"),
    path('minus-item/<int:pk>', views.minus_quantity, name="minus-item"),
    path('plus-item/<int:pk>', views.plus_quantity, name="plus-item"),
    
    path('checkout', views.checkout_item, name="checkout-item"),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    path('order', views.user_order, name="order"),
    path('order-received/<int:pk>', views.item_received, name="order-received"),
    path('order-history', views.order_history, name="order-history"),


    path('create-review/<int:pk>', views.create_review, name="create-review"),
    
    #path('create-checkout', views.create_checkout_session, name="create-checkout"),
    path('stripe-checkout', views.stripe_checkout, name='stripe-checkout'),
    
    # 3 ads path
    path('online-bundles', views.sale_banner_1, name='online-bundles'),
    path('fave-reads',views.sale_banner_2, name='fave-reads'),
    path('special', views.sale_banner_3, name='special'),

    #by_category -- path
    
    path('category-novel', views.genre_novel, name="category-novel"),
    path('category-romance', views.genre_romance, name="category-romance"),
    path('category-science', views.genre_science, name="category-science"),
    path('category-history', views.genre_history, name="category-history"),
    path('shop-by-category/<int:pk>', views.shop_by_category, name="shop-by-category"),

    path('search-item-data', views.search_book, name="search-item-data"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
