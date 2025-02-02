# faq/views.py
from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import FAQ
from .serializers import FAQSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally filter by language and use caching
        """
        lang = self.request.query_params.get('lang')
        
        # Only filter by language if parameter is provided
        if lang:
            # Add debug logging
            print(f"Filtering FAQs for language: {lang}")
            print(f"Current FAQs in DB: {FAQ.objects.values_list('language', flat=True)}")
            
            queryset = FAQ.objects.filter(language=lang)
        else:
            queryset = FAQ.objects.all()
            
        queryset = queryset.order_by("-created_at")
        
        # Debug print
        print(f"Found {queryset.count()} FAQs for language {lang}")
        
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Clear cache after creation
        lang = request.query_params.get("lang", "en")  # Changed from 'language' to 'lang'
        cache.delete(f"faqs_{lang}")
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data})


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Clear cache when updating
        lang = request.query_params.get("lang", "en")
        cache.delete(f"faqs_{lang}")

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Clear cache before deletion
        lang = request.query_params.get("lang", "en")
        cache.delete(f"faqs_{lang}")

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
