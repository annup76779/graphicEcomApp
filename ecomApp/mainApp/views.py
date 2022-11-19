from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
import urllib.parse

from .forms import UploadGraphicsForm
from .models import *
from utility import login_required


def template_cart_data(user):
    if user.is_authenticated:
        return Cart.current_user_cart(user)
    else:
        return None


# Create your views here.
def homepage(request):
    return render(request, 'mainApp/basepage.html',{"tags": Tag.objects.all()})


def index(request):
    tag = request.GET.get('q')
    if tag is not None:
        graphics = Graphics.objects.filter(tag__name=tag).all()
    else:
        graphics = Graphics.objects.all()

    if request.user.is_authenticated:
        graphics_data = [
            (
                graphic,
                len(graphic.wishlist_set.filter(user= request.user)) != 0
            ) for graphic in graphics
        ]
    else:
        graphics_data = [(graphic, False) for graphic in graphics]
    return render(request, 'mainApp/homepage.html',
                  {"graphics": graphics_data, "user": request.user, "cart_data": template_cart_data(request.user)}
                  )


def showcase(request, graphic_id):
    try:
        if graphic_id is not None and graphic_id.isnumeric():
            graphic = Graphics.objects.get(id=int(graphic_id))

            # getting object from review querySet
            if request.user.is_authenticated:
                check_review = Review.objects.filter(user = request.user, graphics = graphic).first()
                if check_review is not None:
                    check_review = True
                else:
                    check_review = False
            else:
                check_review = False
            return render(request, 'mainApp/showcase.html',
                          {"graphic": graphic, "user": request.user, "cart_data": template_cart_data(request.user), "isReviewed": check_review})
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

@login_required
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


@login_required
def give_review(request):
    if request.method == 'POST':
        rate = request.POST.get("rate")
        graphic = request.POST.get("graphic_id")
        review = request.POST.get("review")
        if graphic is not None and graphic.isnumeric():
            # graphics whose review is taken
            graphic = Graphics.objects.get(id=int(graphic))
            if graphic is None:
                messages.error(request, "Graphics doesn't exist.'")
                return redirect("index")
            check_review =Review.objects.filter(graphics = graphic, user = request.user).first()
            if check_review is not None:
                # if there is any review present of the sepecified graphics and the user combo.
                # then we don't want to go further and we will update the rating
                check_review.rate = rate.strip()
                check_review.review = review.strip()
                check_review.save() # updating the rating of the user
                # showing the success message
                messages.success(request, "Review updated successfully.")
            else:
                review = Review(user = request.user, graphics=graphic, rate = rate, review = review.strip())
                # saveing the review to the database
                review.save()
                # showing the success message
                messages.success(request, "Review recorded successfully.")

            # return the valid response.
            return redirect("showcase", graphic_id = int(graphic.id))
        else:
            messages.error(request, "Cannot add reqview for {}".format(graphic))
            return redirect("index")
    else:
        messages.error(request, "Cannot submit this request of review.")
        return redirect("index")


## add to wishlist view function bellow
@login_required
def add_to_wishlist(request, graphic_id):
    wish = request.GET.get("wishlistData")
    if wish is not None and wish.isnumeric():
        wish = int(wish)
        if wish == 0:
            wish_data = Wishlist.objects.filter(graphics__id= graphic_id, user = request.user).first()
            wish_data.delete()
            messages.success(request, "Removed from wishlist")
        else:
            wish_data = Wishlist(graphics = Graphics.objects.get(id=graphic_id), user = request.user)
            wish_data.save()
            messages.success(request, "Added to wishlist")
        return redirect("index")
    else:
        messages.warning(request, "Cannot add to wishlist, invalid wishlist request.")
        return redirect("index")


@login_required
def remove_from_wishlist(request, graphic_id):
    wish = request.GET.get("wishlistData")
    if wish is not None and wish.isnumeric():
        wish = int(wish)
        if wish == 0:
            wish_data = Wishlist.objects.filter(graphics__id= graphic_id, user = request.user).first()
            wish_data.delete()
            messages.success(request, "Removed from wishlist")
    return redirect("wishlist")

@login_required
def wishlist(request):
    wishlist = [[wish.graphics, wish.id] for wish in request.user.wishlist_set.all()]
    return render(request, "mainApp/wishlist.html", {"wishlist": wishlist})


def portfolio(request):
    return render(request, "mainApp/portfolio.html")