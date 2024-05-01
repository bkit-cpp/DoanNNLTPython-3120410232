from django.urls import path
from . import views
from store.controller import authview, cart, checkoutpage, wishlist

urlpatterns = [
    path('', views.home, name="home"),
    path('shop', views.shop,name="shop"),
    path('product-list', views.productlistAjax,name=".productlistAjax"),
    path('searchproduct', views.searchproduct, name="searchproduct"),
    path('contact', views.contact, name="contact"),
    path('shop/<str:slug>', views.shopviews, name="shopviews"),
    path('shop/<str:cate_slug>/<str:prod_slug>', views.productdetails, name="productdetails"),
    path('register/', authview.register, name="register"),
    path('login/', authview.loginpage, name="loginpage"),
    path('logout/', authview.logoutpage, name="logout"),
    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('cart', cart.viewcart, name="cart"),
    path('delete-cart-item', cart.deletecartitem,name="deletecartitem"),
    path('update-cart',cart.updatecart,name="updatecart"),
    path('checkout', cart.checkout, name="checkout"),
    path("reviews/<str:prod_slug>",views.Review_rate, name="Review_rate"),
    path("checkoutpage/",checkoutpage.index, name="checkoutpage"),
    path('place-order', checkoutpage.placeorder,name="placeorder"),
    path('wishlist',wishlist.index,name="wishlist"),
   path('add-to-wishlist/<int:product_id>/',wishlist.add_to_wishlist, name='add_to_wishlist'),
   path('remove-to-wishlist/<int:product_id>/', wishlist.remove_to_wishlist, name='remove_to_wishlist'),
]
