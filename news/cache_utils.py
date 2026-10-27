from django.core.cache import cache
from django.db.models import Count

from .models import Category


def get_cached_categories():
    cache_key = 'news_categories_list'

    categories = cache.get(cache_key)

    if categories is None:
        categories = list(
            Category.objects.annotate(
                news_count=Count('news')
            ).order_by('name').values(
                'id',
                'name',
                'description',
                'news_count'
            )
        )

        cache.set(cache_key, categories, 300)

    return categories


def get_cached_category_counts():
    cache_key = 'news_category_counts'

    counts = cache.get(cache_key)

    if counts is None:
        counts = dict(
            Category.objects.annotate(
                news_count=Count('news')
            ).values_list('id', 'news_count')
        )

        cache.set(cache_key, counts, 300)

    return counts



def clear_news_cache():
    cache.delete('news_categories_list')
    cache.delete('news_category_counts')
    cache.delete('news_list')


    # Очищаем также кешированные страницы списка новостей.

    cache.clear()

