import graphene
import graphene_django_optimizer as gql_optimizer

from graphql import GraphQLError

from . import types
from ...tournament import models, TournamentStatus


def resolve_super_category(info, id):
    return models.SuperCategory.objects.get(pk=id)


def resolve_super_categories(info):
    qs = models.SuperCategory.objects.all().prefetch_related("sub_categories")
    return gql_optimizer.query(qs, info)


def resolve_category(info, id):
    return models.Category.objects.get(pk=id)


def resolve_categories(info):
    qs = models.Category.objects.all()
    return gql_optimizer.query(qs, info)


def resolve_tournament(info, id, code=None):
    """
    Bara hægt að sjá public tournaments nema með kóða.
    """
    user = info.context.user
    if code:
        try:
            return models.Tournament.objects.get(code=code)
        except:
            raise GraphQLError("Invalid code")
    else:
        return models.Tournament.objects.public(user).get(pk=id)


def resolve_tournaments(info):
    user = info.context.user
    qs = (
        models.Tournament.objects.public(user=user)
        .select_related("creator")
        .prefetch_related("admins", "registered_users", "matches")
    )
    return gql_optimizer.query(qs, info)


def resolve_tournament_statuses(info):
    return TournamentStatus.CHOICES


def resolve_match(info, id):
    return models.Match.objects.get(pk=id)


def resolve_matches(info):
    qs = models.Match.objects.all()
    return gql_optimizer.query(qs, info)

