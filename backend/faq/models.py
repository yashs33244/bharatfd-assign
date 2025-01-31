# backend/faq/models.py
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from .translations import translate_text

class FAQ(models.Model):
    """
    Multilingual FAQ model with dynamic translation support
    """
    # Base question and answer in English
    question = models.TextField(_('Question'))
    answer = RichTextField(_('Answer'))

    # Multilingual support fields
    question_hi = models.TextField(_('Question in Hindi'), blank=True, null=True)
    answer_hi = RichTextField(_('Answer in Hindi'), blank=True, null=True)
    
    question_bn = models.TextField(_('Question in Bengali'), blank=True, null=True)
    answer_bn = RichTextField(_('Answer in Bengali'), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Automatically translate content if translation is not provided
        """
        # Translate to Hindi if not provided
        if not self.question_hi:
            self.question_hi = translate_text(self.question, 'hi')
        if not self.answer_hi:
            self.answer_hi = translate_text(self.answer, 'hi')

        # Translate to Bengali if not provided
        if not self.question_bn:
            self.question_bn = translate_text(self.question, 'bn')
        if not self.answer_bn:
            self.answer_bn = translate_text(self.answer, 'bn')

        super().save(*args, **kwargs)

    def get_translated_content(self, lang='en'):
        """
        Dynamically retrieve translated content
        
        :param lang: Language code (en, hi, bn)
        :return: Dict with translated question and answer
        """
        translations = {
            'en': {
                'question': self.question,
                'answer': self.answer
            },
            'hi': {
                'question': self.question_hi or self.question,
                'answer': self.answer_hi or self.answer
            },
            'bn': {
                'question': self.question_bn or self.question,
                'answer': self.answer_bn or self.answer
            }
        }
        
        return translations.get(lang, translations['en'])

    def __str__(self):
        return self.question[:100]

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['-created_at']