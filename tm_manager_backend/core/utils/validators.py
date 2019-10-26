from django import forms

from functools import wraps


def prepare_for_update(form, *args, **kwargs):
    # tökum required af öllum reitum
    for field_key, field_value in form.fields.items():
        field_value.required = False
    # geymum reitina sem á að update-a
    if "data" in kwargs:
        form.fields_to_update = list(kwargs["data"].keys())


def validate_instance(save):
    @wraps(save)
    def func(self, user):
        if not self.instance.pk:
            raise forms.ValidationError("No instance found")
        return save(self, user)

    return func


def validate_fields(save):
    @wraps(save)
    def func(self, user):
        if not self.fields_to_update:
            raise forms.ValidationError("No fields to update")
        return save(self, user)

    return func

