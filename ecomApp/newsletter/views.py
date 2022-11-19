from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Newsletter


# Create your views here.
def newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        if Newsletter.objects.filter(email = email.strip()).exists():
            messages.info(request, "Email already registered for newsletter.")
            return redirect("index")
        newsletter_db_obj = Newsletter(name = name, email = email)
        newsletter_db_obj.save()
        messages.info(request, "Registered for newsletter.")
        return redirect("index")
    else:
        return render(request, "mainApp/newsletter.html")
