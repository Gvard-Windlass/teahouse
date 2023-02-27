from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, verbose_name=_("birthday"))
    avatar = models.ImageField(
        upload_to="user_images/", null=True, blank=True, verbose_name=_("avatar")
    )


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()
