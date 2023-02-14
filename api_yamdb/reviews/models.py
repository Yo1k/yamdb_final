from django.contrib.auth import get_user_model
from django.db import models

# The length of text used in `__str__`
LENGTH_STR = 15
# The length for `CharField`
NAME_MAX_LENGTH = 256
# The length for `SlugField`
SLUG_MAX_LENGTH = 50

User = get_user_model()


class Category(models.Model):
    """
    Categories of artworks.
    """

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    """
    Comments on reviews.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='username автора комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария'
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:LENGTH_STR]


class Genre(models.Model):
    """
    Genres of artworks.
    """

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """
    Reviews of artworks.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='username пользователя'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(score__gte=1)
                    & models.Q(score__lte=10)
                ),
                name='A score value is valid between 1 and 10'
            ),
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='single_review_for_title',
            ),
        ]
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        return self.text[:LENGTH_STR]


class Title(models.Model):
    """
    Name of artwork.
    """

    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
    )
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название',
    )
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Год выпуска',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self) -> str:
        return self.name
