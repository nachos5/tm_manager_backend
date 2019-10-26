from django import forms
from random import shuffle

from . import models
from .utils.validators import validate_creator_or_admin
from ..core.forms import ModelFormCreateOrUpdate
from ..core.utils.validators import (
    prepare_for_update,
    validate_instance,
    validate_fields,
)


class TournamentCreateForm(ModelFormCreateOrUpdate):
    class Meta:
        model = models.Tournament
        fields = ["category", "name", "slots"]

    def save(self, user):
        self.instance.creator = user
        instance = super().save()
        return instance


class TournamentUpdateForm(TournamentCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        prepare_for_update(self, *args, **kwargs)

    @validate_instance
    @validate_fields
    @validate_creator_or_admin
    def save(self, user):
        instance = super().save(user)
        return instance


# addar eða removar (togglar) user úr móti
class TournamentToggleRegisteredUserForm(forms.ModelForm):
    class Meta:
        model = models.Tournament
        fields = []

    @validate_instance
    def save(self, user):
        instance = super().save()
        if user in instance.registered_users.all():
            instance.registered_users.remove(user)
        else:
            instance.registered_users.add(user)
        return instance


# setur userana í tournamentinu í slottin fyrir fyrsta roundið
class TournamentCreateInitialMatchups(forms.ModelForm):
    class Meta:
        model = models.Tournament
        fields = []

    @validate_instance
    @validate_creator_or_admin
    def save(self, user):
        instance = super().save()
        # sækjum round 1 matchana
        first_round_matches = models.Match.objects.filter(
            tournament=instance, level=instance.n_rounds
        )

        # shufflum userunum
        users_shuffled = list(instance.registered_users.all())
        shuffle(users_shuffled)
        # assignum userunum í matchana
        for i, match in enumerate(first_round_matches):
            # sækjum usera til að setja í þennan match
            user_1 = None
            user_2 = None
            if (i * 2) < len(users_shuffled):
                user_1 = users_shuffled[i * 2]
            if (i * 2 + 1) < len(users_shuffled):
                user_2 = users_shuffled[i * 2 + 1]
            # assignum userunum
            if user_1 and user_2:
                match.users.set([user_1, user_2])
            elif user_1:
                match.users.set([user_1])
                break
            else:
                break

        return instance
