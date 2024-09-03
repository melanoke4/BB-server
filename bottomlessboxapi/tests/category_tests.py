from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bottomlessboxapi.models.category import Category

class CategoryViewSetTests(APITestCase):

    def setUp(self):
        # Create some test categories
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Books")
        self.category3 = Category.objects.create(name="Clothing")

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'Electronics')

    def test_create_category(self):
        url = reverse('category-list')
        data = {'name': 'Furniture'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 4)
        self.assertEqual(response.data['name'], 'Furniture')

    def test_create_category_invalid_data(self):
        url = reverse('category-list')
        data = {'name': ''}  # Empty name
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_category(self):
        url = reverse('category-detail', args=[self.category1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics')

    def test_update_category(self):
        url = reverse('category-detail', args=[self.category2.id])
        data = {'name': 'Updated Books'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Books')

    def test_update_category_invalid_data(self):
        url = reverse('category-detail', args=[self.category2.id])
        data = {'name': ''}  # Empty name
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_category(self):
        url = reverse('category-detail', args=[self.category3.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 2)

    def test_search_categories(self):
        url = reverse('category-search')
        response = self.client.get(url, {'name': 'ics'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Electronics')

    def test_search_categories_no_results(self):
        url = reverse('category-search')
        response = self.client.get(url, {'name': 'xyz'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_nonexistent_category(self):
        url = reverse('category-detail', args=[999])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_category(self):
        url = reverse('category-detail', args=[999])  
        data = {'name': 'Non-existent Category'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_category(self):
        url = reverse('category-detail', args=[999])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)