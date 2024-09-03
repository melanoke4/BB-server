from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bottomlessboxapi.models import User

class UserViewTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create(username="testuser", email="test@example.com")

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')

    def test_retrieve_user(self):
        url = reverse('user-detail', args=[self.test_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_create(self):
        url = reverse('user-list')
        data = {'username': 'newuser', 'email': 'new@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['username'], 'newuser')

    def test_update_user(self):
        url = reverse('user-detail', args=[self.test_user.id])
        data = {'username': 'updateduser', 'email': 'updated@example.com'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, 'updateduser')
        self.assertEqual(self.test_user.email, 'updated@example.com')

    def test_delete_user(self):
        url = reverse('user-detail', args=[self.test_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_retrieve_nonexistent_user(self):
        url = reverse('user-detail', args=[999])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_with_existing_username(self):
        url = reverse('user-list')
        data = {'username': 'testuser', 'email': 'another@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_invalid_email(self):
        url = reverse('user-list')
        data = {'username': 'newuser', 'email': 'invalid-email'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(str(response.data['email'][0]), "Enter a valid email address.")