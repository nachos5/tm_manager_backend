import datetime
import math
import random
import string

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from . import TournamentStatus
from ..users.models import User
from .utils.tree import init_single_elim
from .utils.validators import validate_power_of_two, validate_date


class SuperCategory(models.Model):
    """Model definition for SuperCategory."""

    name = models.CharField(max_length=50)

    class Meta:
        """Meta definition for SuperCategory."""

        ordering = ["name"]
        verbose_name = "Super Category"
        verbose_name_plural = "Super Categories"

    def __str__(self):
        """Unicode representation of SuperCategory."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method for SuperCategory."""
        super().save(*args, **kwargs)


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=50)
    super_category = models.ForeignKey(
        SuperCategory, on_delete=models.CASCADE, related_name="sub_categories"
    )

    class Meta:
        """Meta definition for Category."""

        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method for Category."""
        super().save(*args, **kwargs)


# class TournamentQuerySet(models.QuerySet):
#     def filter(self, *args, **kwargs):
#         qs = super().filter(*args, **kwargs)
#         return qs


class Tournament(models.Model):
    """Model definition for Tournament."""

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tournaments"
    )
    admins = models.ManyToManyField(
        User, related_name="admin_for_tournaments", blank=True
    )

    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tournaments"
    )
    name = models.CharField(max_length=50)
    status = models.CharField(
        max_length=32, default=TournamentStatus.OPEN, choices=TournamentStatus.CHOICES
    )
    slots = models.IntegerField(
        default=16,
        validators=[
            MinValueValidator(8),
            MaxValueValidator(256),
            validate_power_of_two,
        ],
    )
    registered_users = models.ManyToManyField(
        User, related_name="tournaments", blank=True
    )
    private = models.BooleanField(default=False)
    code = models.CharField(max_length=8, blank=True)
    location = models.CharField(max_length=100)
    date = models.DateField(validators=[validate_date])
    time = models.TimeField()

    # objects = TournamentQuerySet.as_manager()

    class Meta:
        """Meta definition for Tournament."""

        ordering = ["-created", "-pk"]
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"

    def __str__(self):
        """Unicode representation of Tournament."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method for Tournament."""
        # random 8 stafa strengur
        self.code = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        super().save(*args, **kwargs)
        # búum til matchana fyrir mótið
        # ef við bætum við fleiri formöttum þyrfti að breyta hér
        if self.matches.count() == 0:
            init_single_elim(self)

    @property
    def n_rounds(self):
        # fjöldi leikja fyrsta roundið
        n_matches = int(self.slots / 2)
        # fjöldi umferða er base 2 logrinn af fjölda leikja round 1
        n_rounds = int(math.log(n_matches, 2))
        return n_rounds


class MatchQuerySet(models.QuerySet):
    def first_round_matches(self, tournament_id):
        return self.filter(
            tournament_id=tournament_id,
            # filterum eftir max lvl-inu fyrir þetta tournament
            level=self.filter(tournament_id=tournament_id).aggregate(
                models.Max("level")
            )["level__max"],
        )


class Match(MPTTModel):
    """Model definition for Match."""

    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="matches"
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    user_home = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="home_matches",
        blank=True,
        null=True,
    )
    user_visitor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="visitor_matches",
        blank=True,
        null=True,
    )
    user_home_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    user_visitor_points = models.IntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="matches_won",
        blank=True,
        null=True,
    )

    custom_objects = MatchQuerySet.as_manager()

    class Meta:
        """Meta definition for Match."""

        ordering = ["tournament__pk", "level"]
        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        """Unicode representation of Match."""
        return "{t} - Match #{pk}".format(t=self.tournament.name, pk=self.pk)

    def save(self, *args, **kwargs):
        """Save method for Match."""
        super().save(*args, **kwargs)

    @property
    def users(self):
        if self.user_home:
            if self.user_visitor:
                return [self.user_home, self.user_visitor]
            return [self.user_home]
        return []
