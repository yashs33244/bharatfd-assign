from typing import Optional

from django.core.cache import cache
from googletrans import Translator


class TranslationService:
    def __init__(self):
        self.translator = Translator()
        self.cache_timeout = 24 * 60 * 60  # 24 hours

    def get_translation(self, text: str, target_lang: str) -> str:
        """Get translation with caching support"""
        if not text:
            return text

        cache_key = f"trans_{hash(text)}_{target_lang}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            translation = self.translator.translate(text, dest=target_lang)
            translated_text = translation.text
            cache.set(cache_key, translated_text, self.cache_timeout)
            return translated_text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def bulk_translate(self, texts: list, target_lang: str) -> list:
        """Bulk translate multiple texts"""
        return [self.get_translation(text, target_lang) for text in texts]


translator_service = TranslationService()


def translate_text(text: str, target_lang: str) -> str:
    return translator_service.get_translation(text, target_lang)
