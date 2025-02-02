from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FAQ

class FAQEndpointTestCase(TestCase):
    def setUp(self):
        # Clear any existing data
        FAQ.objects.all().delete()
        
        # Create test data
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
            question="জ্যাঙ্গো কি?",
            answer="জ্যাঙ্গো একটি ওয়েব ফ্রেমওয়ার্ক।",
            language="bn"
        )
        
        self.client = APIClient()

    def test_faq_list_endpoint(self):
        response = self.client.get('/api/faqs/')  # Correct URL for the FAQ list
        self.assertEqual(len(response.data["results"]), 3, f"Expected 3 FAQs, got {len(response.data['results'])}")

    def test_faq_detail_endpoint(self):
        """Test retrieving a single FAQ"""
        url = reverse("faq-detail", kwargs={"pk": self.faq1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["question"], "What is Django?")

    def test_create_faq_endpoint(self):
        """Test creating a new FAQ"""
        initial_count = FAQ.objects.count()
        url = reverse("faq-list")
        data = {
            "question": "What is REST?",
            "answer": "REST is an architectural style for designing APIs.",
            "language": "en"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FAQ.objects.count(), initial_count + 1)

        new_faq = FAQ.objects.latest("id")
        self.assertEqual(new_faq.question, "What is REST?")

    def test_update_faq_endpoint(self):
        """Test updating an existing FAQ"""
        url = reverse("faq-detail", kwargs={"pk": self.faq1.id})
        data = {
            "question": "Updated Django Question",
            "answer": "Updated answer about Django.",
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh from database and verify update
        self.faq1.refresh_from_db()
        self.assertEqual(self.faq1.question, "Updated Django Question")

    def test_delete_faq_endpoint(self):
        """Test deleting a FAQ"""
        initial_count = FAQ.objects.count()
        url = reverse("faq-detail", kwargs={"pk": self.faq1.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FAQ.objects.count(), initial_count - 1)

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

