import datetime
import math

from functools import wraps

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _("%(value)s is not an even number"), params={"value": value}
        )


def validate_power_of_two(value):
    power_of_two = math.log(value, 2).is_integer()
    if not power_of_two:
        raise ValidationError("{value} is not a power of 2".format(value=value))


def validate_date(value):
    if value < datetime.date.today():
        raise ValidationError("The date cannot be in the past!")


def validate_creator_or_admin(save):
    @wraps(save)
    def func(self, user):
        # aðeins sá sem bjó til tournamentið eða admins geta editað (eða superuser)
        if (
            not user == self.instance.creator
            and not user in self.instance.admins.all()
            and not user.is_superuser
        ):
            raise forms.ValidationError("You can't modify this tournament")
        return save(self, user)

    return func


def validate_creator_or_admin_match(save):
    @wraps(save)
    def func(self, user):
        # aðeins sá sem bjó til tournamentið eða admins geta editað (eða superuser)
        if (
            not user == self.instance.tournament.creator
            and not user in self.instance.tournament.admins.all()
            and not user.is_superuser
        ):
            raise forms.ValidationError("You can't modify this tournament")
        return save(self, user)

    return func
