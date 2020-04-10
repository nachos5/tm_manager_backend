from django.db.models import Q
from django_filters import FilterSet, NumberFilter, CharFilter

from ...tournament import models


class CategoryFilter(FilterSet):
    class Meta:
        model = models.Category
        fields = {
            "name": ["iexact", "icontains"],
            "super_category__name": ["iexact", "icontains"],
        }


class TournamentFilter(FilterSet):
    creator = NumberFilter(method="creator_filter")
    registered_in = NumberFilter(method="registered_in_filter")
    super_category = NumberFilter(method="super_category_filter")
    search = CharFilter(method="search_filter")

    def creator_filter(self, queryset, name, value):
        print(value)
        return queryset.filter(creator_id=value)

    def registered_in_filter(self, queryset, name, value):
        return queryset.filter(registered_users__in=[value])

    def super_category_filter(self, queryset, name, value):
        return queryset.filter(category__super_category__pk=value)

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(category__name__icontains=value)
        )

    class Meta:
        model = models.Tournament
        fields = {
            "name": ["iexact", "icontains"],
            "status": ["iexact", "in"],
            "category__name": ["iexact", "in"],
        }
