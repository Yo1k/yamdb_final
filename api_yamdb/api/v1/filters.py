from django_filters import rest_framework as df_filters
from reviews.models import Title


class TitleFilter(df_filters.FilterSet):
    name = df_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    genre = df_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    category = df_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )

    class Meta:
        fields = ['name', 'genre', 'category', 'year']
        model = Title
