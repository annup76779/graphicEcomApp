from django.shortcuts import render
from django.http import HttpResponse

from .forms import UploadGraphicsForm
# Create your views here.
def index(request):
    return render(request, 'mainApp/upload.html', {"form": UploadGraphicsForm()})