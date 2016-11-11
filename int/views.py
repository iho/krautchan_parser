# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from rest_framework import routers

from .models import Post

from rest_framework import (filters, generics, mixins, permissions, status,

                            viewsets, serializers)


from django.shortcuts import render
router = routers.SimpleRouter()
# Create your views here.

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # filter_backends = (filters.OrderingFilter,)
    # ordering_fields = '__all__'
    permission_classes = [] # [permissions.IsAuthenticated]
    filter_fields = ('country_code', 'date', 'id', 'text', 'main_post', 'url')
class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(main_post=True)
    serializer_class = PostSerializer
    filter_fields = ('country_code', 'date', 'id', 'text', 'main_post', 'url')

router.register(r'threads', ThreadViewSet, base_name='threads')
router.register(r'posts', PostViewSet, base_name='posts')

urlpatterns = router.urls
