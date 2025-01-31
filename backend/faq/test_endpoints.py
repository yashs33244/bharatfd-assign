# backend/faq/tests_endpoints.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import FAQ

class FAQEndpointTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test FAQs
        self.faq1 = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework for Python."
        )
        self.faq2 = FAQ.objects.create(
            question="How to create a model?",
            answer="Use Django's model class to define database schema."
        )

    def test_faq_list_endpoint(self):
        """Test retrieving list of FAQs"""
        url = reverse('faq-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_faq_detail_endpoint(self):
        """Test retrieving a single FAQ"""
        url = reverse('faq-detail', kwargs={'pk': self.faq1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['question'], "What is Django?")

    def test_multilingual_endpoint(self):
        """Test language-specific FAQ retrieval"""
        url = reverse('faq-list')
        
        # Test English (default)
        response_en = self.client.get(url, {'lang': 'en'})
        self.assertEqual(response_en.status_code, 200)
        
        # Test Hindi
        response_hi = self.client.get(url, {'lang': 'hi'})
        self.assertEqual(response_hi.status_code, 200)

    def test_create_faq_endpoint(self):
        """Test creating a new FAQ"""
        url = reverse('faq-list')
        data = {
            'question': "What is REST?",
            'answer': "REST is an architectural style for designing APIs."
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FAQ.objects.count(), 3)

    def test_update_faq_endpoint(self):
        """Test updating an existing FAQ"""
        url = reverse('faq-detail', kwargs={'pk': self.faq1.id})
        data = {
            'question': "Updated Django Question",
            'answer': "Updated answer about Django."
        }
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, 200)
        updated_faq = FAQ.objects.get(id=self.faq1.id)
        self.assertEqual(updated_faq.question, "Updated Django Question")

    def test_delete_faq_endpoint(self):
        """Test deleting a FAQ"""
        url = reverse('faq-detail', kwargs={'pk': self.faq1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FAQ.objects.count(), 1)