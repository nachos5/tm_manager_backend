import graphene
import graphql_jwt

from graphene_django.forms.mutation import DjangoModelFormMutation

from . import types
from ...users import forms


class TokenCreateMutation(graphql_jwt.ObtainJSONWebToken):
    user = graphene.Field(types.User)

    def resolve_user(self, info):
        return info.context.user


class UserCreateMutation(DjangoModelFormMutation):
    tournament = graphene.Field(types.User)

    class Meta:
        form_class = forms.UserCreationForm
