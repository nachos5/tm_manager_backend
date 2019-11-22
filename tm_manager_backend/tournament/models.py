import math

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from . import TournamentStatus
from ..users.models import User
from .utils.tree import init_single_elim
from .utils.validators import validate_power_of_two


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

    class Meta:
        """Meta definition for Tournament."""

        ordering = ["pk"]
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"

    def __str__(self):
        """Unicode representation of Tournament."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method for Tournament."""
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


class Match(MPTTModel):
    """Model definition for Match."""

    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="matches"
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    # viljum bara tvo usera þannig að setjum validation í clean aðferð
    users = models.ManyToManyField(User, related_name="matches", blank=True)
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="matches_won",
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Match."""

        ordering = ["tournament__pk", "level"]
        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        """Unicode representation of Match."""
        return "{t} - Match #{pk}".format(t=self.tournament.name, pk=self.pk)

    def clean(self):
        if self.pk and self.users and self.users.count() > 2:
            raise ValidationError("Only two users are allowed per match.")

    def save(self, *args, **kwargs):
        """Save method for Match."""
        super().save(*args, **kwargs)
