from .views import *
from django.urls import path


urlpatterns = [
    
    path('api/sitelogo/', SiteLogoAPIView.as_view(), name='logo-list'),
    path('api/nav/',  NavOptionAPIVIEW.as_view(), name = 'nav_list'),
    path('api/button/', ButtonAPIVIEW.as_view(), name = 'button_list'),

    path('categories/home/', HomeCategoryAPIView.as_view()),
    path('categories/', CategoryListAPIView.as_view()),

    path('products/home/', HomeProductAPIView.as_view(), name='home-products'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),

    path('new-arrivals/home/', HomeNewArrivalAPIView.as_view(), name='home-new-arrivals'),
    path('new-arrivals/', NewArrivalListAPIView.as_view(), name='new-arrival-list'),
    

    path('newsletter/subscribe/', NewsletterSubscriberAPIVIEW.as_view(), name='newsletter-subscribe'),
    
    path('cart/', CartAPIView.as_view(), name='cart-detail'),
    path('cart/summary/', CartSummaryAPIView.as_view(), name='cart-summary'),
    path('cart/add/', AddToCartAPIView.as_view(), name='add-to-cart'),     
    path('cart/items/<int:item_id>/update', UpdateCartItemAPIView.as_view(), name='update-cart-item'),  # PUT / DELETE
    path('cart/items/<int:item_id>/remove', RemoveCartItemAPIView.as_view(), name= 'remove-cart-item'),

    path('orders/', UserOrderListAPIView.as_view(), name='user-orders'),
    path('orders/<int:order_id>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('orders/place/', PlaceOrderAPIView.as_view(), name='place-order'),

    #path('checkout/', PlaceOrderAPIView.as_view()),

    path('reviews/create/', ReviewCreateAPIView.as_view(), name='create-review'),
]