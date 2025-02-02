from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FAQ

class FAQEndpointTestCase(TestCase):
    def setUp(self):
        # Creating FAQ objects in different languages
        self.faq1 = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework.",
            question_hi="Django क्या है?",
            answer_hi="Django एक वेब फ्रेमवर्क है।",
            question_bn="Django কি?",
            answer_bn="Django একটি ওয়েব ফ্রেমওয়ার্ক।",
            language="en"
        )
        self.faq2 = FAQ.objects.create(
            question="How to create a model?",
            answer="Use Django's model class to define database schema.",
            question_hi="एक मॉडल कैसे बनाएं?",
            answer_hi="डेटाबेस स्कीमा को परिभाषित करने के लिए Django के मॉडल वर्ग का उपयोग करें।",
            question_bn="কিভাবে একটি মডেল তৈরি করবেন?",
            answer_bn="ডাটাবেস স্কিমা সংজ্ঞায়িত করতে জ্যাঙ্গোর মডেল ক্লাস ব্যবহার করুন।",
            language="en"
        )
        self.faq3 = FAQ.objects.create(
            question="Django কী?",
            answer="Django হল Python এর জন্য একটি ওয়েব ফ্রেমওয়ার্ক।",
            question_hi="Django क्या है?",
            answer_hi="Django पायथन के लिए एक वेब फ्रेमवर्क है।",
            question_bn="Django কী?",
            answer_bn="Django হল Python এর জন্য একটি ওয়েব ফ্রেমওয়ার্ক।",
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
    # Test fetching FAQs in specific language
        response = self.client.get('/faq/', {'language': 'en'})  # Adjust your endpoint
        print(response.data)  # Log the response for debugging
        self.assertEqual(len(response.data["results"]), 2, f"Expected 2 FAQs for 'en', got {len(response.data['results'])}")
        
        response_bn = self.client.get('/faq/', {'language': 'bn'})  # For Bengali language
        self.assertEqual(len(response_bn.data["results"]), 1, f"Expected 1 FAQ for 'bn', got {len(response_bn.data['results'])}")
        
        response_hi = self.client.get('/faq/', {'language': 'hi'})  # For Hindi language
        self.assertEqual(len(response_hi.data["results"]), 1, f"Expected 1 FAQ for 'hi', got {len(response_hi.data['results'])}")

