from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from members.models import Profile

from .forms import UserRegistrationForm, ProfileForm


def registerTemplate(request):
    """
        Save the user registration form from the template to the auth_user table and then can be used to login user.
        Username, password and email will be the parameters of the posted data.
    """
    return render(request, 'members/register.html', {"form": UserRegistrationForm()})
 

def postUserRegistrationHere(request):
    if request.method == "POST":
        registration_form_instance = UserRegistrationForm(request.POST)
        if registration_form_instance.is_valid():
            cleaned_data = registration_form_instance.cleaned_data
            if not User.objects.filter(username = cleaned_data["username"]).exists() and not User.objects.filter( email = cleaned_data["email"]).exists():
                user = User.objects.create_user(**cleaned_data)
                user.save()
                messages.success(request,"Party dued party")
            else:
                messages.error(request, "User already exists.")
        else:
            messages.warning(request, "Please fill all the required fields.")
        return redirect(registerTemplate)
    else:
        return "Method not allowed."


def login_user(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            messages.warning(request, "This you cannot pass this page as superuser.")
            return redirect(registerTemplate)
    print(request.user.is_superuser)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect("index")
        else:
            messages.info(request, "There was an error loggin in, Try again.")
            return redirect(login_user)
    else:
        return render(request, "members/login.html")


# logout the user
def logout_user(request):
    logout(request)
    messages.info(request, "User logged out.")


def profile_page(request):
    if request.method == "POST":
        try:
            profile = Profile.objects.get(user=request.user)
            profile.delete()
        except Profile.DoesNotExist:
            pass
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        print(form_data)
        profile_form = ProfileForm(form_data)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user =request.user
            profile.save()
            return redirect('index')
        else:
            messages.error(request, "Please will all the details properly.")
            return redirect('profile')
    else:
        form = ProfileForm()
        return render(request, "members/profile.html", {"form": form})