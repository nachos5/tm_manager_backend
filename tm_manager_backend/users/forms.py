from django import forms as django_forms

from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    set_as_superuser = django_forms.BooleanField(required=False)

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "name")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise ValidationError("This field is required")
        return email

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name:
            raise ValidationError("This field is required")
        return name

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])

    def save(self, *args, **kwargs):
        c = self.cleaned_data
        if "set_as_superuser" in c:
            s = c.pop("set_as_superuser")
        instance = super().save(*args, **kwargs)
        print(instance)
        if s:
            instance.is_superuser = True
            instance = instance.save()
        print(instance)
        return instance
