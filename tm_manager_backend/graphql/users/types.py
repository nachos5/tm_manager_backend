import graphene

from ..core.types import CountableDjangoObjectType
from ...users import models


class User(CountableDjangoObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.User

