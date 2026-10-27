from django.shortcuts import render
from django.core.cache import cache
from django.http import Http404
from .cache_utils import get_cached_categories
# Create your views here.
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import News, Category

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import NewsForm
from .cache_utils import clear_news_cache



class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']

    def get_queryset(self):
        return News.objects.select_related(
            'category', 'author'
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_cached_categories()
        return context




class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.select_related(
            'category', 'author'
        )

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        user_key = (
            self.request.user.pk
            if self.request.user.is_authenticated
            else 'anonymous'
        )

        cache_key = f'news_detail_{self.kwargs["pk"]}_user_{user_key}'

        news_object = cache.get(cache_key)

        if news_object is None:
            try:
                news_object = queryset.get(pk=self.kwargs['pk'])
            except News.DoesNotExist:
                raise Http404('Новость не найдена')

            cache.set(cache_key, news_object, 300)

        return news_object




class CategoryListView(ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return get_cached_categories()


class NewsCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    permission_required = 'news.add_news'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        clear_news_cache()
        return response


class NewsUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    permission_required = 'news.change_news'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        clear_news_cache()
        return response


class NewsDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    model = News
    template_name = 'news/news_confirm_delete.html'
    permission_required = 'news.delete_news'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        clear_news_cache()
        return response
