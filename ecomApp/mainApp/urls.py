from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name = "homepage"),
    path('app/', views.index, name = 'index'),
    path("app/showcase/<graphic_id>", views.showcase, name = 'showcase'),
    path("app/add_to_cart", views.add_to_cart, name = 'add_to_cart'),
    path("app/update_cart/<cart_id>", views.update_cart, name = 'update_cart'),
    path("app/detete_from_cart/<cart_id>", views.delete_from_cart, name = 'delete_cart'),
    path("give_review", views.give_review, name = 'give_review')
]

