import json

import graphene

from .filters import CategoryFilter, TournamentFilter
from .utils import match_bracket
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
    match_bracket = graphene.String()

    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Tournament
        filterset_class = TournamentFilter

    def resolve_status_display(self, info):
        return self.get_status_display()

    def resolve_match_bracket(self, info):
        """ setur bracketinn á form eins og react-tournament-bracket biður um """
        matches = self.matches.all().order_by("level")
        # rótin er winnerinn
        root = matches.first()
        d = match_bracket(root)
        return json.dumps(d)


class MatchType(CountableDjangoObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Match
