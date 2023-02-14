from datetime import datetime

from django.http import Http404
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Category


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
        read_only_fields = (
            'author',
            'id',
            'pub_date',
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        model = Review
        read_only_fields = (
            'id',
            'pub_date',
        )

    def validate(self, data):
        """
        Checks that an author can create only one review for a specific title.
        """
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')

        if (
            self.context.get('request').method == 'POST'
            and author.reviews.filter(title=title_id).exists()
        ):
            raise serializers.ValidationError(
                'You can only have one review for a particular title'
                ' and you already have one'
            )

        return data

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                'A score value is valid between 1 and 10'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugField(max_length=50, required=False)
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        required=False,
        slug_field='slug'
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title
        read_only_fields = (
            'id',
            'rating',
        )

    def __get_category(self, category_data):
        if category_data:
            try:
                return get_object_or_404(
                    Category,
                    slug=category_data,
                )

            except Http404:
                raise serializers.ValidationError(
                    f'There is no such category {category_data}'
                )
        return None

    def __save_related_genres(self, genres_data, obj):
        if genres_data:
            obj.genre.set(genres_data)

    def create(self, validated_data):
        category_data = validated_data.pop('category', None)
        genres_data = validated_data.pop('genre', None)

        title = Title.objects.create(
            category=self.__get_category(category_data),
            **validated_data
        )
        title.save()
        self.__save_related_genres(genres_data, title)

        return title

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        genres_data = validated_data.pop('genre', None)
        category = self.__get_category(category_data)

        if category:
            instance.category = category
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description',
            instance.description
        )

        instance.save()
        self.__save_related_genres(genres_data, instance)

        return instance

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer()
        self.fields['genre'] = GenreSerializer(many=True)
        return super().to_representation(instance)

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'The year of the title can not be greater'
                ' than the current year'
            )
        return value
