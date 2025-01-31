# backend/faq/views.py
from rest_framework import viewsets
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer

class FAQViewSet(viewsets.ModelViewSet):
    """
    Viewset for FAQ with caching and multilingual support
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        """
        Optionally filter by language and use caching
        """
        lang = self.request.query_params.get('lang', 'en')
        cache_key = f'faqs_{lang}'

        # Try to get from cache first
        cached_faqs = cache.get(cache_key)
        if cached_faqs is not None:
            return cached_faqs

        # If not in cache, query and cache
        faqs = FAQ.objects.all()
        cache.set(cache_key, faqs, timeout=3600)  # Cache for 1 hour
        return faqs