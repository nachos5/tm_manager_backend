from django_filters import FilterSet, NumberFilter

from ...tournament import models


class CategoryFilter(FilterSet):
    class Meta:
        model = models.Category
        fields = {
            "name": ["iexact", "icontains"],
            "super_category__name": ["iexact", "icontains"],
        }


class TournamentFilter(FilterSet):
    super_category = NumberFilter(method="super_category_filter")

    def super_category_filter(self, queryset, name, value):
        return queryset.filter(category__super_category__pk=value)

    class Meta:
        model = models.Tournament
        fields = {
            "name": ["iexact", "icontains"],
            "status": ["iexact", "in"],
            "category__name": ["iexact", "in"],
        }
