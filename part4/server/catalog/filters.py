from django_filters.rest_framework import CharFilter, FilterSet, RangeFilter

from .models import Wine, WineSearchWord


class WineFilterSet(FilterSet):
    price = RangeFilter()
    query = CharFilter(method='filter_query')

    def filter_query(self, queryset, name, value):
        return queryset.search(value)

    class Meta:
        model = Wine
        fields = ('query', 'country', 'points', 'price',)


class WineSearchWordFilterSet(FilterSet):
    query = CharFilter(method='filter_query')

    def filter_query(self, queryset, name, value):
        return queryset.search(value)

    class Meta:
        model = WineSearchWord
        fields = ('query',)
