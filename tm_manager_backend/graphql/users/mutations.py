import graphene

from graphene_django.forms.mutation import DjangoModelFormMutation

from . import types
from ...users import forms


class UserCreateMutation(DjangoModelFormMutation):
    tournament = graphene.Field(types.User)

    class Meta:
        form_class = forms.UserCreationForm
