from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bottomlessboxapi.models.user import User
from bottomlessboxapi.models.item import Item
from bottomlessboxapi.models.category import Category
from bottomlessboxapi.models.location import Location
from bottomlessboxapi.models.status import Status

class ItemViewSetTests(APITestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create(username='user1', email="test1@example.com")
        self.user2 = User.objects.create(username='user2', email="test2@example.com")

        # Create test categories
        self.category1 = Category.objects.create(name='Electronics')
        self.category2 = Category.objects.create(name='Books')

        # Create test locations
        self.location = Location.objects.create(name='Home')

        # Create test statuses
        self.status = Status.objects.create(name='In Use')

        # Create test items
        self.item1 = Item.objects.create(
            user=self.user1,
            name='Laptop',
            cost=10,
            purchase_date='2023-01-01',
            location=self.location,
            status=self.status
        )
        self.item1.categories.add(self.category1)

        self.item2 = Item.objects.create(
            user=self.user2,
            name='Book',
            cost=20,
            purchase_date='2023-02-01',
            location=self.location,
            status=self.status
        )
        self.item2.categories.add(self.category2)

    def test_list_items(self):
        url = reverse('item-list')
        # self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_items_filtered_by_user(self):
        url = reverse('item-list')
        # self.client.force_authenticate(user=self.user1)
        response = self.client.get(url, {'user_id': self.user1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Laptop')

    def test_create_item(self):
        url = reverse('item-list')
        # self.client.force_authenticate(user=self.user1)
        data = {
            'user_id': self.user1.id,
            'name': 'New Item',
            'cost': 50,
            'purchase_date': '2023-03-01',
            'categories': [self.category1.id],
            'location': self.location.id,
            'status': self.status.id,
            'image_url': 'www.image.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 3)
        self.assertEqual(response.data['name'], 'New Item')

    def test_create_item_invalid_user(self):
        url = reverse('item-list')
        # self.client.force_authenticate(user=self.user1)
        data = {
            'user_id': 999,  # Non-existent user
            'name': 'New Item',
            'cost': 50,
            'purchase_date': '2023-03-01',
            'categories': [self.category1.id],
            'location': self.location.id,
            'status': self.status.id,
            'image_url': 'www.image.com'
            
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_item(self):
        url = reverse('item-detail', args=[self.item1.id])
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop')

    def test_retrieve_item_unauthorized(self):
        url = reverse('item-detail', args=[self.item1.id])
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        url = reverse('item-detail', args=[self.item1.id])
        self.client.force_authenticate(user=self.user1)
        data = {'name': 'Updated Laptop'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Laptop')

    def test_update_item_unauthorized(self):
        url = reverse('item-detail', args=[self.item1.id])
        self.client.force_authenticate(user=self.user2)
        data = {'name': 'Unauthorized Update'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item(self):
        url = reverse('item-detail', args=[self.item1.id])
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 1)

    def test_delete_item_unauthorized(self):
        url = reverse('item-detail', args=[self.item1.id])
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Item.objects.count(), 2)
