import graphene
import graphene_django_optimizer as gql_optimizer

from graphql import GraphQLError

from . import types
from ...users import models


def resolve_me(info):
    user = info.context.user
    if user.is_authenticated:
        return user
    else:
        return None


def resolve_user(info, id):
    return models.User.objects.get(pk=id)


def resolve_users(info):
    qs = models.User.objects.all()
    return gql_optimizer.query(qs, info)

