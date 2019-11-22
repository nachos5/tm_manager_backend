import graphene

from .filters import CategoryFilter, TournamentFilter
from ..core.types import CountableDjangoObjectType
from ...tournament import models


class SuperCategoryType(CountableDjangoObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.SuperCategory


class CategoryType(CountableDjangoObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Category
        filterset_class = CategoryFilter


class TournamentType(CountableDjangoObjectType):
    status_display = graphene.String()

    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Tournament
        filterset_class = TournamentFilter

    def resolve_status_display(self, info):
        return self.get_status_display()


class MatchType(CountableDjangoObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Match
