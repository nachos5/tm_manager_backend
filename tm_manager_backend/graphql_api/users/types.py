import graphene
import graphene_django_optimizer as gql_optimizer

from ..core.types import CountableDjangoObjectType
from ...tournament.models import Match, Tournament
from ...users import models


class User(CountableDjangoObjectType):
    id_int = graphene.Int()
    matches_won_count = graphene.Int()
    tournaments_won_count = graphene.Int()

    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.User
        exclude = ("password", "isSuperuser", "isStaff", "isActive")

    def resolve_id_int(self, info):
        return info.context.user.id

    def resolve_tournaments(self, info):
        user = info.context.user
        if self == user:
            qs = self.tournaments.all()
        else:
            qs = self.tournaments.public(user)

        return gql_optimizer.query(qs, info)

    def resolve_created_tournaments(self, info):
        user = info.context.user
        if self == user:
            qs = self.created_tournaments.all()
        else:
            qs = self.created_tournaments.public(user)

        return gql_optimizer.query(qs, info)

    def resolve_matches_won_count(self, info):
        user = info.context.user
        if user.is_authenticated:
            return Match.objects.filter(winner=user).count()
        return 0

    def resolve_tournaments_won_count(self, info):
        user = info.context.user
        if user.is_authenticated:
            return Tournament.objects.filter(winner=user).count()
        return 0
