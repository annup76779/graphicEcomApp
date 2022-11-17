from django.contrib import admin
from .models import Graphics, Tag, Cart
# Register your models here.
admin.site.register(Graphics)
admin.site.register(Tag)
# admin.site.register(Order)
admin.site.register(Cart)