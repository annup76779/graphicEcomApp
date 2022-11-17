from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
import urllib.parse

from .forms import UploadGraphicsForm
from .models import *


def template_cart_data(user):
    if user.is_authenticated:
        return Cart.current_user_cart(user)
    else:
        return None


# Create your views here.
def homepage(request):
    tag = request.GET.get('q')
    if tag is not None:
        graphics = Graphics.objects.filter(tag__name=tag).all()
    else:
        graphics = Graphics.objects.all()
    return render(request, 'mainApp/basepage.html',
                  {"graphics": graphics, "user": request.user, "cart_data": template_cart_data(request.user)}
                  )


def index(request):
    tag = request.GET.get('q')
    if tag is not None:
        graphics = Graphics.objects.filter(tag__name=tag).all()
    else:
        graphics = Graphics.objects.all()
    return render(request, 'mainApp/homepage.html',
                  {"graphics": graphics, "user": request.user, "cart_data": template_cart_data(request.user)}
                  )


def showcase(request, graphic_id):
    try:
        if graphic_id is not None and graphic_id.isnumeric():
            graphic = Graphics.objects.get(id=int(graphic_id))
            return render(request, 'mainApp/showcase.html',
                          {"graphic": graphic, "user": request.user, "cart_data": template_cart_data(request.user)})
        else:
            return redirect('index')
    except Graphics.DoesNotExist:
        return redirect("index")


def add_to_cart(request):
    if not request.user.is_authenticated:
        messages.info(request, "You must be logged in to add to cart.")
        response = redirect('login_user')
        response["location"] += "?" + urllib.parse.urlencode({"next": f"showcase?s={request.POST.get('graphics_id)')}"})
        return response
    print("?" + urllib.parse.urlencode({"next": f"showcase?s={request.POST.get('graphics_id)')}"}))
    add_on = request.POST.get("add_on")
    quantity = request.POST.get("quantity")
    graphic_id = request.POST.get("graphic_id")
    try:
        graphic_id = int(graphic_id)
    except ValueError:
        messages.info(request, "Invalid graphic id.")
    try:
        graphic = Graphics.objects.get(id=int(graphic_id))
    except Graphics.DoesNotExist:
        messages.error(request, "This Graphics is not available.")
    cart = Cart.objects.filter(graphics=graphic, user=request.user).first()
    try:
        if cart is None:
            messages.success(request, "Added to cart.")
            cart = Cart(note=add_on, quantity=quantity, graphics=graphic, user=request.user)
            cart.save()
        else:
            cart.note = add_on
            cart.quantity = quantity
            cart.save()
            messages.info(request, "Cart updated")
    except Exception as error:
        messages.error(request, f"{str(error)} Cannot add to cart, something went wrong.")
    return redirect("index")


def update_cart(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        quantity = request.GET.get("q")
        cart.quantity = int(quantity)
        cart.save()
        count, _, total = template_cart_data(request.user)
        return JsonResponse(status=200, data=dict(status=True, msg="Cart Updated.", delta_cost=total, count=count))
    except ValueError as error:
        print(error)
        return JsonResponse(status=200, data=dict(status=False, msg="Cannot must be number."))
    except Exception as error:
        print(error)
        return JsonResponse(status=200, data=dict(status=False, msg="Something went wrong."))


def delete_from_cart(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        count, _, total = template_cart_data(request.user)
        return JsonResponse(status=200,
                            data={'status': True, "msg": "Successfully deleted", "delta_cost": total, "count": count})
    except Exception as error:
        return JsonResponse(status=200, data=dict(status=False, msg="Something went wrong"))


def give_review(request):
    if request.user.is_authenticated:
        rate = request.GET.get("review")
        graphic = request.GET.get("graphic_id")
        if graphic is not None and graphic.isnumeric():
            graphic = Graphics.objects.get(id=int(graphic))
            messages.success(request, "Review recorded successfully.")
            return redirect("showcase", graphic_id = int(graphic.id))
        else:
            messages.error(request, "Cannot add reqview for {}".format(graphic))
            return redirect("index")

    else:
        return redirect("login_user")
