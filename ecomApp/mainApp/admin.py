from django.contrib import admin
from .models import Graphics, Tag, Cart, Review, Contact, Testimonial, Wishlist

# Register your models here.
admin.site.register(Graphics)
admin.site.register(Tag)
# admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(Testimonial)
admin.site.register(Wishlist)
