from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save
from django.contrib.auth.models import User
import os


# BLOCK: Database block

# start first commit of this file
class Tag(models.Model):  # consider as category
    name = models.CharField(max_length=100, null=False, unique=True, default="Other")

    def __str__(self):
        return self.name


class Graphics(models.Model):
    title = models.CharField(max_length=200)
    cost = models.FloatField(max_length=20, default=0.0)
    discount = models.FloatField(max_length=4, null=True, blank=True)
    discription = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=1)  # category of graphic from tag table
    media = models.FileField()
    pub_date = models.DateField(auto_now_add=True)  # upload date.

    def __str__(self):
        return f"{self.id}) {self.title if len(self.title) < 50 else self.title[:49] + '...'}, COST: {self.cost} {'with discount' + str(self.discount) + '%' if self.discount is not None and self.discount > 0 else ''}"


# SIGNALS
# https://docs.djangoproject.com/en/4.1/topics/signals/#connecting-to-signals-sent-by-specific-senders
@receiver(pre_delete, sender=Graphics)
def delete_graphics_on_graphics_delete(sender, instance, **kwargs):
    '''dipatcher to delete the graphics when the graphics object is deleted from admin side'''
    if instance.media:  # if there is any media in graphics object
        instance.media.delete(False)  # then delete it.


@receiver(pre_save, sender=Graphics)
def delete_graphics_on_graphics_update(sender, instance, **kwargs):
    '''
        dipatcher to update the graphics with the new graphics if there is any new graphics
        upload for any existing graphics id.
    '''
    if instance._state.adding and not instance.pk:  # graphics exists already
        return False

    try:
        previous_media = sender.objects.get(pk=instance.pk).media
    except sender.DoesNotExist:
        return False
    if not instance.media == previous_media:  # the new media is not equal to previous_media
        if os.path.isfile(previous_media.path):  # and the originally exists
            os.remove(previous_media.path)  # delete it.


# end the first commit

# SIGNALS END

class Cart(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['graphics', 'user'], name='unique_cart_item')
        ]

    graphics = models.ForeignKey(Graphics, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank=False, null=False, default=1)
    date_to_cart = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.graphics.title} - {self.quantity} by {self.user.username}"

    @staticmethod
    def get_count_of_current_user(user: User) -> int:
        cart = Cart.objects.filter(user=user)
        if cart is not None:
            return cart.count()
        else:
            return 0

    @staticmethod
    def current_user_cart(user: User) -> tuple:
        """
            Takes the User object of the requesting user and then return are actuall cart with count of
            elements in it.

            In case there is not item in the cart then the tuple returned will be (0, None)
            else
                if there are items in the cart then 
                Returns: tuple[int, QuerySet]
        """

        if isinstance(user, User):
            cart = Cart.objects.filter(user=user)
            if cart is not None:
                total_cost_of_cart = 0
                for cart_item in cart:
                    total_cost_of_cart += cart_item.total_cost()
                return cart.count(), cart, total_cost_of_cart
            else:
                return None
        else:
            raise AttributeError("user accepted is of type User.")

    def total_cost(self):
        """Returns the total cost of the item after reducing discount"""
        discount = self.graphics.discount if self.graphics.discount is not None else 0
        return round((self.graphics.cost - (self.graphics.cost * (discount / 100))) * self.quantity, 2)

    def to_dict(self):
        return dict(
            product_id=self.graphics.id,
            user=self.user.id,
            quantity=self.quantity,
            note=self.note,
        )


class Review(models.Model):
    Choices = (
        ("1", "1 star"),
        ("2", "2 star"),
        ("3", "3 star"),
        ("4", "4 star"),
        ("5", "5 star"),

    )
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    graphics = models.ForeignKey(Graphics, null=False, blank=False, on_delete=models.CASCADE)
    rate = models.CharField(choices=Choices, max_length=1, null=False, blank=False)
    review = models.TextField(null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['graphics', 'user'], name='unique_review')
        ]


class Wishlist(models.Model):
    """The support for the Wishlist"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["graphics", "user"], name='unique_wishlisth')
        ]

    graphics = models.ForeignKey(Graphics, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Testimonial(models.Model):
    """testimonial will be added by the admin from admin"""
    user = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    media = models.FileField(upload_to="testimonial")
