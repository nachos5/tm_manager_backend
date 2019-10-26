import graphene

from .filters import TournamentFilter
from ..core.types import CountableDjangoObjectType
from ...tournament import models


class SuperCategory(CountableDjangoObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.SuperCategory


class Category(CountableDjangoObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Category


class Tournament(CountableDjangoObjectType):
    status_display = graphene.String()

    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Tournament
        filterset_class = TournamentFilter

    def resolve_status_display(self, info):
        return self.get_status_display()


class Match(CountableDjangoObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Match
