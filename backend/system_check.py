import os

import django
from celery.app.base import Celery
from django.core.cache import cache
from redis import Redis


def test_redis_connection():
    """Test Redis connection"""
    try:
        redis_client = Redis(host="localhost", port=6379, db=0)
        redis_client.ping()
        print("✅ Redis connection successful")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False


def test_django_cache():
    """Test Django cache framework"""
    try:
        cache.set("test_key", "test_value", 30)
        value = cache.get("test_key")
        if value == "test_value":
            print("✅ Django cache working")
            return True
        else:
            print("❌ Django cache not working properly")
            return False
    except Exception as e:
        print(f"❌ Django cache error: {e}")
        return False


def test_celery_connection():
    """Test Celery configuration"""
    try:
        app = Celery("core")
        app.config_from_object("django.conf:settings", namespace="CELERY")
        print("✅ Celery configuration loaded")
        return True
    except Exception as e:
        print(f"❌ Celery configuration error: {e}")
        return False


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()

    print("\nRunning system checks...\n")
    redis_ok = test_redis_connection()
    cache_ok = test_django_cache()
    celery_ok = test_celery_connection()

    print("\nSystem Check Summary:")
    print("-" * 20)
    print(f"Redis: {'✅' if redis_ok else '❌'}")
    print(f"Cache: {'✅' if cache_ok else '❌'}")
    print(f"Celery: {'✅' if celery_ok else '❌'}")
