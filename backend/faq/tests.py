# backend/faq/tests.py
import pytest
from django.test import TestCase
from .models import FAQ
from .translations import translate_text

@pytest.mark.django_db
class FAQModelTestCase(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a high-level Python web framework."
        )

    def test_faq_creation(self):
        """Test FAQ object creation"""
        self.assertTrue(isinstance(self.faq, FAQ))
        self.assertEqual(self.faq.__str__(), self.faq.question[:100])

    def test_multilingual_translation(self):
        """Test dynamic translation retrieval"""
        # Check English retrieval
        en_content = self.faq.get_translated_content('en')
        self.assertEqual(en_content['question'], "What is Django?")

        # Check Hindi translation
        hi_content = self.faq.get_translated_content('hi')
        self.assertIsNotNone(hi_content['question'])

    def test_translation_utility(self):
        """Test translation function"""
        translated_text = translate_text("Hello", 'hi')
        self.assertIsNotNone(translated_text)
        self.assertNotEqual(translated_text, "Hello")

@pytest.mark.django_db
class FAQAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.faq = FAQ.objects.create(
            question="Test Question",
            answer="Test Answer"
        )

    def test_faq_list_endpoint(self):
        """Test FAQ list API endpoint"""
        response = self.client.get('/api/faqs/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())

    def test_multilingual_endpoint(self):
        """Test language query parameter"""
        response = self.client.get('/api/faqs/?lang=hi')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())