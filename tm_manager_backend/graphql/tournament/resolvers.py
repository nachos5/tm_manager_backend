import graphene
import graphene_django_optimizer as gql_optimizer

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


def resolve_tournament(info, id):
    return models.Tournament.objects.get(pk=id)


def resolve_tournaments(info):
    qs = models.Tournament.objects.filter(private=False).prefetch_related(
        "registered_users", "matches"
    )
    return gql_optimizer.query(qs, info)


def resolve_tournament_statuses(info):
    return TournamentStatus.CHOICES


def resolve_match(info, id):
    return models.Match.objects.get(pk=id)


def resolve_matches(info):
    qs = models.Match.objects.all().prefetch_related("users")
    return gql_optimizer.query(qs, info)

