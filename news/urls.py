from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path(
        '',
        cache_page(60 * 5)(views.NewsListView.as_view()),
        name='news_list',
    ),
    path(
        'news/<int:pk>/',
        views.NewsDetailView.as_view(),
        name='news_detail',
    ),
    path(
        'categories/',
        views.CategoryListView.as_view(),
        name='category_list',
    ),
    path(
        'news/create/',
        views.NewsCreateView.as_view(),
        name='news_create',
    ),
    path(
        'news/<int:pk>/edit/',
        views.NewsUpdateView.as_view(),
        name='news_update',
    ),
    path(
        'news/<int:pk>/delete/',
        views.NewsDeleteView.as_view(),
        name='news_delete',
    ),
]

