from django.contrib import admin

# Register your models here.
from .models import Category, News


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
