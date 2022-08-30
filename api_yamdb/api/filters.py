
from django_filters import rest_framework as filters
from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """Создаем собственный класс для фильтрации по связанным полям"""
    pass


class TitleFilter(filters.FilterSet):
    """Создаем собственный класс для фильтрации по полям Title"""
    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')
    category = CharFilterInFilter(
        field_name='category__slug',
        lookup_expr='in'
    )
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['genre', 'year', 'name', ]
