import csv
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

CSV_DIR = os.path.join(
    settings.BASE_DIR,
    'static',
    'data',
)

TABLES = {
    User: {
        'path': 'users.csv',
        'headers': (
            'id', 'username', 'email', 'role', 'bio', 'first_name',
            'last_name',
        ),
    },
    Category: {
        'path': 'category.csv',
        'headers': ('id', 'name', 'slug'),
    },
    Genre: {
        'path': 'genre.csv',
        'headers': ('id', 'name', 'slug'),
    },
    Title: {
        'path': 'titles.csv',
        'headers': ('id', 'name', 'year', 'category_id'),
    },
    Title.genre.through: {
        'path': 'genre_title.csv',
        'headers': ('id', 'title_id', 'genre_id'),
    },
    Review: {
        'path': 'review.csv',
        'headers': (
            'id', 'title_id', 'text', 'author_id', 'score', 'pub_date'
        ),
    },
    Comment: {
        'path': 'comments.csv',
        'headers': ('id', 'review_id', 'text', 'author_id', 'pub_date'),
    },
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model, file in TABLES.items():
            with open(
                file=os.path.join(CSV_DIR, file['path']),
                encoding='utf-8'
            ) as csvfile:
                reader = csv.DictReader(
                    csvfile,
                    fieldnames=file['headers']
                )
                next(reader)
                try:
                    model.objects.bulk_create(
                        [model(**data) for data in reader],
                        ignore_conflicts=True
                    )
                except Exception as e:
                    print(e, file=sys.stderr)
                else:
                    self.stdout.write(
                        self.style.SUCCESS('Successfully fill in DB')
                    )
