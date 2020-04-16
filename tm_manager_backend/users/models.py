from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    email = EmailField(_("email address"), unique=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self
