from django.core.cache import cache
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

from .models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            "id",
            "question",
            "answer",
            "question_hi",
            "answer_hi",
            "question_bn",
            "answer_bn",
            "created_at",
            "updated_at",
        ]
        fields = '__all__'

    def get_queryset(self):
        """
        Get FAQs with optional language filtering and caching
        """
        lang = self.request.query_params.get("lang", "en")
        cache_key = f"faqs_{lang}"

        # Try to get from cache
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset

        # If not in cache, get from database
        queryset = FAQ.objects.all().order_by("-created_at")
        cache.set(cache_key, queryset, timeout=3600)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        List FAQs with proper pagination
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        Clear cache when updating FAQ
        """
        instance = serializer.save()
        # Clear cache for all supported languages
        for lang in ["en", "hi", "bn"]:
            cache.delete(f"faqs_{lang}")
        return instance
