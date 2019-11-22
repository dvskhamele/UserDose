from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # When In Global.
    name = CharField(_("Name of User"), blank=True, max_length=255)
