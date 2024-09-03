from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bottomlessboxapi.models.category import Category
from bottomlessboxapi.models.item import Item
from bottomlessboxapi.models.location import Location
from bottomlessboxapi.models.review import Review
from bottomlessboxapi.models import User
from django.contrib.auth import get_user_model

from bottomlessboxapi.models.status import Status


class ReviewViewSetTests(APITestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create(username='user1', email="test1@example.com")
        self.user2 = User.objects.create(username='user2', email="test2@example.com")
        
        self.category = Category.objects.create(name='Electronics')

        # Create test locations
        self.location = Location.objects.create(name='Home')

        # Create test statuses
        self.status = Status.objects.create(name='In Use')

         # Create test items
        self.item1 = Item.objects.create(user=self.user1,
                                         name='Item 1',
                                         cost=50.00,
                                         purchase_date='2023-03-01',
                                         # categories=[self.category.id],
                                         location=self.location,
                                         status=self.status,
                                         image_url='www.image.com')
        self.item2 = Item.objects.create(user=self.user2, name='Item 2',
                                         cost=50.00,
                                         purchase_date='2023-03-01',
                                         # categories=[self.category.id],
                                         location=self.location,
                                         status=self.status,
                                         image_url='www.image.com')


        # Create test reviews
        self.review1 = Review.objects.create(item=self.item1, content='Review 1')
        self.review2 = Review.objects.create(item=self.item2, content='Review 2')

    def test_create_review(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('review-list')
        data = {'item': self.item1.id, 'content': 'New Review'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 3)
        self.assertEqual(response.data['content'], 'New Review')

    def test_create_review_invalid_data(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('review-list')
        data = {'item': self.item1.id}  # Missing content
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_review_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('review-detail', args=[self.review1.id])
        data = {'item': self.item1.id, 'content': 'Updated Review'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review1.refresh_from_db()
        self.assertEqual(self.review1.content, 'Updated Review')

    def test_update_review_non_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('review-detail', args=[self.review1.id])
        data = {'item': self.item1.id, 'content': 'Unauthorized Update'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('review-detail', args=[self.review1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 1)

    def test_delete_review_non_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('review-detail', args=[self.review1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Review.objects.count(), 2)

    def test_list_reviews(self):
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_review(self):
        url = reverse('review-detail', args=[self.review1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Review 1')