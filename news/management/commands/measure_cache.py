from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext

from news.cache_utils import get_cached_categories


class Command(BaseCommand):
    help = 'Сравнение SQL-запросов при кешировании категорий'

    def handle(self, *args, **options):
        cache.delete('news_categories_list')

        with CaptureQueriesContext(connection) as queries_before:
            get_cached_categories()

        with CaptureQueriesContext(connection) as queries_after:
            get_cached_categories()

        self.stdout.write(
            f'Запросов без прогретого кеша: {len(queries_before)}'
        )
        self.stdout.write(
            f'Запросов с прогретым кешем: {len(queries_after)}'
        )
