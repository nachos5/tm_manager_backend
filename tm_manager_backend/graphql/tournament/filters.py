from django_filters import FilterSet, NumberFilter

from ...tournament import models


class TournamentFilter(FilterSet):
    super_category = NumberFilter(method="super_category_filter")

    def super_category_filter(self, queryset, name, value):
        return queryset.filter(category__super_category__pk=value)

    class Meta:
        model = models.Tournament
        fields = {"name": ["iexact", "icontains"]}
