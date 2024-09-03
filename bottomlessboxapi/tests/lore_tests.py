from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bottomlessboxapi.models.category import Category
from bottomlessboxapi.models.item import Item
from bottomlessboxapi.models.location import Location
from bottomlessboxapi.models.lore import Lore
from bottomlessboxapi.models.status import Status
from bottomlessboxapi.models.user import User

# User = get_user_model()


class LoreViewSetTests(APITestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create(
            username='user1', email="test1@example.com")
        self.user2 = User.objects.create(
            username='user2', email="test2@example.com")

        # Create test categories
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

        # Create test lores
        self.lore1 = Lore.objects.create(item=self.item1, content='Lore 1')
        self.lore2 = Lore.objects.create(item=self.item2, content='Lore 2')

    def test_list_lores(self):
        url = reverse('lore-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_lores_filtered_by_item(self):
        url = reverse('lore-list')
        response = self.client.get(url, {'item_id': self.item1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Lore 1')

    def test_create_lore(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('lore-list')
        data = {'item': self.item1.id, 'content': 'New Lore'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lore.objects.count(), 3)
        self.assertEqual(response.data['content'], 'New Lore')

    def test_create_lore_invalid_data(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('lore-list')
        data = {'item': self.item1.id}  # Missing content
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_lore_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('lore-detail', args=[self.lore1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Lore 1')

    def test_retrieve_lore_non_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('lore-detail', args=[self.lore1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lore_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('lore-detail', args=[self.lore1.id])
        data = {'item': self.item1.id, 'content': 'Updated Lore'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lore1.refresh_from_db()
        self.assertEqual(self.lore1.content, 'Updated Lore')

    def test_update_lore_non_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('lore-detail', args=[self.lore1.id])
        data = {'item': self.item1.id, 'content': 'Unauthorized Update'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lore_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('lore-detail', args=[self.lore1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lore.objects.count(), 1)

    def test_delete_lore_non_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('lore-detail', args=[self.lore1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lore.objects.count(), 2)
