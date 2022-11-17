from functools import wraps
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def login_required(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if args[0].user.is_authenticated:
            return fun(*args, **kwargs)
        else:
            return redirect("login_user")

    return wrapper