from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class SouvenirAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_html_photo', 'price', 'availability')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_editable = ('availability',)
    list_filter = ('price', 'availability')
    prepopulated_fields = {"slug": ("title", )}
    fields = ('title', 'slug', 'cat', 'description', 'photo', 'get_html_photo', 'availability')
    readonly_fields = ('get_html_photo',)
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50")

    get_html_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name", )}

admin.site.register(Souvenir, SouvenirAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель магазина сувениров'
admin.site.site_header = 'Админ-панель магазина сувениров'