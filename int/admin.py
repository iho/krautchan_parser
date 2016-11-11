# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        u'date',
        u'text',
        u'url',
        u'thread',
        u'country_code',
        u'country_path',
        u'main_post',
    )
    list_filter = (u'date',)
admin.site.register(Post, PostAdmin)
