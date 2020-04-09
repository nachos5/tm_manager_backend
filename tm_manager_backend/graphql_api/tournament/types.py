import json

import graphene

from .filters import CategoryFilter, TournamentFilter
from .utils import match_bracket
from ..core.types import CountableDjangoObjectType
from ..users.types import User
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
    user_is_registered = graphene.Boolean()
    can_edit = graphene.Boolean()
    winner = graphene.Field(User)
    n_rounds = graphene.Int()

    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Tournament
        filterset_class = TournamentFilter

    def resolve_status_display(self, info):
        return self.get_status_display()

    def resolve_match_bracket(self, info):
        """ setur bracketinn á form eins og react-tournament-bracket biður um """
        matches = self.matches.all()
        matches = list(matches)
        users = self.registered_users.all()
        # rótin er winnerinn
        root = matches[-1]
        d = match_bracket(root, matches, users)
        j = json.dumps(d, indent=2)
        # print(j)
        return j

    def resolve_user_is_registered(self, info):
        user = info.context.user
        if user.is_authenticated and user in self.registered_users.all():
            return True
        return False

    def resolve_can_edit(self, info):
        user = info.context.user
        return user.is_authenticated and (
            user.is_superuser or user == self.creator or user in self.admins.all()
        )

    def resolve_n_rounds(self, info):
        return self.n_rounds

    def resolve_winner(self, info):
        return self.winner

    def resolve_code(self, info):
        user = info.context.user
        # ef private tourn. geta ekki allir séð
        if (
            self.private
            and not user == self.creator
            and not user in self.admins.all()
            and not user.is_superuser
        ):
            return "private"
        return self.code


class MatchType(CountableDjangoObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]
        model = models.Match
