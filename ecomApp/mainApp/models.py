from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete

class Graphics(models.Model):
    title = models.CharField(max_length=200)
    cost = models.FloatField(max_length=20, default=0.0)
    discount = models.FloatField(max_length=4, null=True, blank = True)
    discription = models.TextField()
    media = models.FileField()
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}) {self.title if len(self.title) < 50 else self.title[:49]+'...'}, COST: {self.cost} {'with discount'+str(self.discount)+'%' if self.discount is not None and self.discount > 0 else ''}"


# https://docs.djangoproject.com/en/4.1/topics/signals/#connecting-to-signals-sent-by-specific-senders
@receiver(pre_delete, sender=Graphics)
def delete_graphics_on_graphics_delete(sender, instance, **kwargs):
    '''dipatcher to delete the graphics when the graphics object is deleted from admin side'''
    if instance.media:
        instance.media.delete(False)