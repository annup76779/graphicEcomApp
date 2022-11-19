from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name = "home"),
    path('app/', views.index, name = 'index'),
    path("app/showcase/<graphic_id>", views.showcase, name = 'showcase'),
    path("app/add_to_cart", views.add_to_cart, name = 'add_to_cart'),
    path("app/update_cart/<cart_id>", views.update_cart, name = 'update_cart'),
    path("app/delete_from_cart/<cart_id>", views.delete_from_cart, name = 'delete_cart'),
    path("app/give_review", views.give_review, name = 'give_review'),
    path("app/add_to_wishlist/<graphic_id>", views.add_to_wishlist, name = 'add_to_wishlist'),
    path("app/wishlist", views.wishlist, name = 'wishlist'),
    path("app/remove_from_wishlist/<graphic_id>", views.remove_from_wishlist, name = 'remove_from_wishlist'),
    path("portfolio", views.portfolio, name = 'portfolio'),
]
