from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bottomlessboxapi.models import Status

class StatusViewSetTests(APITestCase):

    def setUp(self):
        # Create some test statuses
        self.status1 = Status.objects.create(name="Status1")
        self.status2 = Status.objects.create(name="Status2")

    def test_list_statuses(self):
        url = reverse('status-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Status1')
        self.assertEqual(response.data[1]['name'], 'Status2')

    def test_create_status(self):
        url = reverse('status-list')
        data = {'name': 'NewStatus'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 3)
        self.assertEqual(response.data['name'], 'NewStatus')

    def test_retrieve_status(self):
        url = reverse('status-detail', args=[self.status1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Status1')

    def test_delete_status(self):
        url = reverse('status-detail', args=[self.status2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Status.objects.count(), 1)

    def test_create_invalid_status(self):
        url = reverse('status-list')
        data = {'name': ''}  # Invalid empty name
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_status(self):
        url = reverse('status-detail', args=[999]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_status(self):
        url = reverse('status-detail', args=[999]) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)