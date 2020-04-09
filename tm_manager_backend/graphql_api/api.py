import graphene

from .tournament.schema import TournamentMutations, TournamentQueries
from .users.schema import UsersMutations, UsersQueries


class Query(TournamentQueries, UsersQueries):
    pass


class Mutations(TournamentMutations, UsersMutations):
    pass


schema = graphene.Schema(Query, Mutations)
