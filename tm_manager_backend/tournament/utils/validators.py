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


def validate_creator_or_admin(save):
    @wraps(save)
    def func(self, user):
        # aðeins sá sem bjó til tournamentið eða admins geta editað
        if not user == self.instance.creator and not user in self.instance.admins.all():
            raise forms.ValidationError("You can't modify this tournament")
        return save(self, user)

    return func
