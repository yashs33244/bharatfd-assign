from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from .translations import translate_text


class FAQ(models.Model):
    """
    Multilingual FAQ model with dynamic translation support.
    """
    language = models.CharField(max_length=10)  # or use a choice field for languages
    question = models.TextField()
    answer = models.TextField()
    question_hi = models.TextField(null=True, blank=True)
    answer_hi = models.TextField(null=True, blank=True)
    question_bn = models.TextField(null=True, blank=True)
    answer_bn = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Adding language field with choices
    # language = models.CharField(
    #     _("Language"),
    #     max_length=10,
    #     choices=[("en", "English"), ("hi", "Hindi"), ("bn", "Bengali")],
    #     default="en"
    # )
    # question = models.CharField(max_length=255)
    # answer = models.TextField()
    
    # # Multilingual fields
    # question_hi = models.CharField(max_length=255, blank=True)
    # answer_hi = models.TextField(blank=True)
    
    # question_bn = models.CharField(max_length=255, blank=True)
    # answer_bn = models.TextField(blank=True)
    
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Automatically translate content if translation fields are empty.
        """
        try:
            if not self.question_hi:
                self.question_hi = translate_text(self.question, "hi") or self.question
            if not self.answer_hi:
                self.answer_hi = translate_text(self.answer, "hi") or self.answer

            if not self.question_bn:
                self.question_bn = translate_text(self.question, "bn") or self.question
            if not self.answer_bn:
                self.answer_bn = translate_text(self.answer, "bn") or self.answer
        except Exception as e:
            print(f"Translation error: {e}")  # Debugging (log this in production)

        super().save(*args, **kwargs)

    def get_translated_content(self, lang="en"):
        """
        Dynamically retrieve translated content.

        :param lang: Language code (en, hi, bn)
        :return: Dict with translated question and answer.
        """
        translations = {
            "en": {"question": self.question, "answer": self.answer},
            "hi": {"question": self.question_hi or self.question, "answer": self.answer_hi or self.answer},
            "bn": {"question": self.question_bn or self.question, "answer": self.answer_bn or self.answer},
        }

        return translations.get(lang, translations["en"])

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ["-created_at"]
