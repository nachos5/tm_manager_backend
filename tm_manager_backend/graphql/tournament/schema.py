import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import types
from .mutations import (
    TournamentCreateMutation,
    TournamentUpdateMutation,
    TournamentToggleRegisteredUserMutation,
    TournamentCreateInitialMatchupsMutation,
)
from . import resolvers
from ..core.fields import PrefetchingConnectionField


class TournamentQueries(graphene.ObjectType):
    super_category = graphene.Field(
        types.SuperCategoryType,
        id=graphene.Argument(graphene.ID),
        description="Returns a single Super Category by ID.",
    )
    super_categories = PrefetchingConnectionField(
        types.SuperCategoryType, description="Returns a list of Super Category nodes."
    )

    category = graphene.Field(
        types.CategoryType,
        id=graphene.Argument(graphene.ID),
        description="Returns a single Category node by ID.",
    )
    categories = DjangoFilterConnectionField(
        types.CategoryType, description="Returns a list of Category nodes."
    )

    tournament = graphene.Field(
        types.TournamentType,
        id=graphene.Argument(graphene.ID),
        description="Returns a single Tournament node.",
    )
    tournaments = DjangoFilterConnectionField(
        types.TournamentType, description="Returns a list of Tournament nodes."
    )
    tournament_statuses = graphene.List(
        graphene.List(graphene.String),
        description="Returns all available Tournament statuses in a list, where each element is a tuple on the format [status, status display text]",
    )

    match = graphene.Field(
        types.MatchType,
        id=graphene.Argument(graphene.ID),
        description="Returns a single Match by ID.",
    )
    matches = PrefetchingConnectionField(
        types.MatchType, description="Returns a list of Match nodes."
    )

    def resolve_super_category(self, info, id, **kwargs):
        return resolvers.resolve_super_category(info, id)

    def resolve_super_categories(self, info, **kwargs):
        return resolvers.resolve_super_categories(info)

    def resolve_category(self, info, id, **kwargs):
        return resolvers.resolve_category(info, id)

    def resolve_categories(self, info, **kwargs):
        return resolvers.resolve_categories(info)

    def resolve_tournament(self, info, id, **kwargs):
        return resolvers.resolve_tournament(info, id)

    def resolve_tournaments(self, info, **kwargs):
        return resolvers.resolve_tournaments(info)

    def resolve_tournament_statuses(self, info, **kwargs):
        return resolvers.resolve_tournament_statuses(info)

    def resolve_match(self, info, id, **kwargs):
        return resolvers.resolve_match(info, id)

    def resolve_matches(self, info, **kwargs):
        return resolvers.resolve_matches(info)


class TournamentMutations(graphene.ObjectType):
    tournament_create = TournamentCreateMutation.Field()
    tournament_update = TournamentUpdateMutation.Field()
    tournament_toggle_registered_user = TournamentToggleRegisteredUserMutation.Field()
    tournament_create_initial_matchups = TournamentCreateInitialMatchupsMutation.Field()

