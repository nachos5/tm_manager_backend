from random import shuffle

from django import forms
from django.db.models import F, Max, Subquery

from . import TournamentStatus
from . import models
from .utils.tree import parent_seeding, free_match_win
from .utils.validators import validate_creator_or_admin, validate_creator_or_admin_match
from ..core.forms import ModelFormCreateOrUpdate
from ..core.utils.validators import (
    prepare_for_update,
    validate_instance,
    validate_fields,
)


class TournamentCreateForm(ModelFormCreateOrUpdate):
    class Meta:
        model = models.Tournament
        fields = ["category", "name", "slots", "date", "time", "location", "private"]

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
        # tournamentið verður að vera opið
        if not instance.status == TournamentStatus.OPEN:
            raise forms.ValidationError("This tournament is not open for registration.")
        # togglum
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
        self.instance.status = TournamentStatus.ONGOING
        instance = super().save()
        # sækjum round 1 matchana
        first_round_matches = models.Match.custom_objects.first_round_matches(
            tournament_id=instance.id
        )

        # shufflum userunum
        users_shuffled = list(instance.registered_users.all())
        shuffle(users_shuffled)
        # assignum userunum í matchana
        updated_matches = []
        free_match = None
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
                match.user_home = user_1
                match.user_visitor = user_2
                updated_matches.append(match)
            elif user_1:
                match.user_home = user_1
                updated_matches.append(match)
                free_match = match
                break
            else:
                break

        # bulk update-um matchana
        models.Match.objects.bulk_update(updated_matches, ["user_home", "user_visitor"])
        if free_match:
            free_match_win(free_match)

        return instance


class MatchCompleteForm(forms.ModelForm):
    class Meta:
        model = models.Match
        fields = ["user_home_points", "user_visitor_points"]

    @validate_instance
    @validate_creator_or_admin_match
    def save(self, user):
        if not (self.instance.user_home and self.instance.user_visitor):
            raise forms.ValidationError("There are not two users in this match!")
        # stillum winner
        if self.instance.user_home_points > self.instance.user_visitor_points:
            self.instance.winner = self.instance.user_home
        elif self.instance.user_home_points < self.instance.user_visitor_points:
            self.instance.winner = self.instance.user_visitor
        else:
            raise forms.ValidationError(
                "The winner can't be determined when there is a draw!"
            )
        instance = super().save()

        parent_seeding(match=instance)
        if not instance.parent.users_both_sides:
            free_match_win(instance.parent)
