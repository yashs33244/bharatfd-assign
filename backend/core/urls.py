# backend/core/urls.py
from django.contrib import admin
from django.urls import include, path
from faq.views import FAQViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"faqs", FAQViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
