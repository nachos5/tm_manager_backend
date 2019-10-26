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
        types.SuperCategory, id=graphene.Argument(graphene.ID)
    )
    super_categories = PrefetchingConnectionField(types.SuperCategory)

    category = graphene.Field(types.Category, id=graphene.Argument(graphene.ID))
    categories = PrefetchingConnectionField(types.Category)

    tournament = graphene.Field(types.Tournament, id=graphene.Argument(graphene.ID))
    tournaments = DjangoFilterConnectionField(types.Tournament)

    match = graphene.Field(types.Match, id=graphene.Argument(graphene.ID))
    matches = PrefetchingConnectionField(types.Match)

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

    def resolve_match(self, info, id, **kwargs):
        return resolvers.resolve_match(info, id)

    def resolve_matches(self, info, **kwargs):
        return resolvers.resolve_matches(info)


class TournamentMutations(graphene.ObjectType):
    tournament_create = TournamentCreateMutation.Field()
    tournament_update = TournamentUpdateMutation.Field()
    tournament_toggle_registered_user = TournamentToggleRegisteredUserMutation.Field()
    tournament_create_initial_matchups = TournamentCreateInitialMatchupsMutation.Field()

