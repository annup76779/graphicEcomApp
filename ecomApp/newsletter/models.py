from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from datetime import datetime

from threading import Thread


# Create your models here.
class Newsletter(models.Model):
    email = models.CharField(max_length=200, null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, default="User")
    red_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-red_date',)


class SendEmail(models.Model):
    subject = models.TextField(null=False, blank=False, default="Newsletter from Graphico")
    body = models.TextField(null=False, blank=False)
    submit_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.subject


@receiver(post_save, sender=SendEmail)
def delete_graphics_on_graphics_update(sender, instance, **kwargs):
    """
        senf newsletter mail to all the recipients at the schduled time.
    """
    send_mail(
        instance.subject,
        instance.body,
        from_email=None,
        recipient_list = [str(email) for email in Newsletter.objects.all()]
    )
