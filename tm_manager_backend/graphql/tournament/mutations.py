import graphene

from graphene_django.forms.mutation import DjangoModelFormMutation

from . import types
from ..core.mutations import DjangoModelFormMutationUser
from ...tournament import forms


class TournamentCreateMutation(DjangoModelFormMutationUser):
    tournament = graphene.Field(types.TournamentType)

    class Meta:
        form_class = forms.TournamentCreateForm


class TournamentUpdateMutation(DjangoModelFormMutationUser):
    tournament = graphene.Field(types.TournamentType)

    class Meta:
        form_class = forms.TournamentUpdateForm


class TournamentToggleRegisteredUserMutation(DjangoModelFormMutationUser):
    tournament = graphene.Field(types.TournamentType)

    class Meta:
        form_class = forms.TournamentToggleRegisteredUserForm


class TournamentCreateInitialMatchupsMutation(DjangoModelFormMutationUser):
    tournament = graphene.Field(types.TournamentType)

    class Meta:
        form_class = forms.TournamentCreateInitialMatchups


class MatchCompleteMutation(DjangoModelFormMutationUser):
    match = graphene.Field(types.MatchType)

    class Meta:
        form_class = forms.MatchCompleteForm
