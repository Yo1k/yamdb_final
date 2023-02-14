from django.db.models import Avg
from django.db.models.functions import Round
from django_filters import rest_framework as df_filters
from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from reviews.models import Category, Genre, Review, Title
from users.permissions import (IsAdministrator, IsAuthorOrReadOnly,
                               IsModerator, ReadOnly)

from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


# Utils
class GenericTitleSubstructViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    lookup_value_regex = '[-a-zA-Z0-9_]+'
    permission_classes = [IsAdministrator | ReadOnly]
    search_fields = ['name']


# Main

class CategoryViewSet(GenericTitleSubstructViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdministrator | IsModerator | IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )


class GenreViewSet(GenericTitleSubstructViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdministrator | IsModerator | IsAuthorOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = (df_filters.DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAdministrator | ReadOnly]
    queryset = Title.objects.annotate(
        rating=Round(Avg('reviews__score'), precision=2)
    )
    serializer_class = TitleSerializer
