import pytest
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import FAQ


@pytest.mark.django_db
class FAQModelTestCase(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a high-level Python web framework.",
        )

    def test_faq_creation(self):
        """Test FAQ object creation"""
        self.assertTrue(isinstance(self.faq, FAQ))
        self.assertEqual(self.faq.__str__(), self.faq.question[:100])

    def test_multilingual_endpoint(self):
    # Test fetching FAQs in English (Correct endpoint and query parameter)
        response = self.client.get('/api/faqs/', {'lang': 'en'})
        self.assertEqual(len(response.data["results"]), 2, f"Expected 2 FAQs for 'en', got {len(response.data['results'])}")

        # Test fetching FAQs in Bengali (Ensure these FAQs exist in the database)
        response_bn = self.client.get('/api/faqs/', {'lang': 'bn'})
        self.assertEqual(len(response_bn.data["results"]), 1, f"Expected 1 FAQ for 'bn', got {len(response_bn.data['results'])}")

        # Test fetching FAQs in Hindi
        response_hi = self.client.get('/api/faqs/', {'lang': 'hi'})
        self.assertEqual(len(response_hi.data["results"]), 1, f"Expected 1 FAQ for 'hi', got {len(response_hi.data['results'])}")



@pytest.mark.django_db
class FAQModelTestCase(TestCase):
    def setUp(self):
        self.faq1 = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework.",
            language="en"
        )
        self.faq2 = FAQ.objects.create(
            question="How to create a model?",
            answer="Use Django's model class.",
            language="en"
        )
        self.faq3 = FAQ.objects.create(
            question="Django কী?",
            answer="Django হল Python এর জন্য একটি ওয়েব ফ্রেমওয়ার্ক।",
            language="bn"
        )
        self.client = APIClient()

    def test_faq_list_endpoint(self):
        """Test FAQ list API endpoint"""
        response = self.client.get("/api/faqs/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    def test_multilingual_endpoint(self):
        # Print current data in database for debugging
        print("\nCurrent FAQs in database:")
        for faq in FAQ.objects.all():
            print(f"ID: {faq.id}, Language: {faq.language}, Question: {faq.question}")
            
        # Test English FAQs
        response_en = self.client.get('/api/faqs/', {'lang': 'en'})
        print(f"\nEnglish response data: {response_en.data}")
        self.assertEqual(
            len(response_en.data["results"]), 
            2, 
            f"Expected 2 FAQs for 'en', got {len(response_en.data['results'])}"
        )
        
        # Test Bengali FAQs
        response_bn = self.client.get('/api/faqs/', {'lang': 'bn'})
        print(f"\nBengali response data: {response_bn.data}")
        self.assertEqual(
            len(response_bn.data["results"]), 
            1, 
            f"Expected 1 FAQ for 'bn', got {len(response_bn.data['results'])}"
        )
