from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bottomlessboxapi.models.location import Location

class LocationViewSetTests(APITestCase):

    def setUp(self):
        # Create some test locations
        self.location1 = Location.objects.create(name="Home")
        self.location2 = Location.objects.create(name="Office")

    def test_list_locations(self):
        url = reverse('location-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Home')
        self.assertEqual(response.data[1]['name'], 'Office')

    def test_create_location(self):
        url = reverse('location-list')
        data = {'name': 'Garage'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 3)
        self.assertEqual(response.data['name'], 'Garage')

    def test_create_location_invalid_data(self):
        url = reverse('location-list')
        data = {'name': ''}  # Empty name
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_location(self):
        url = reverse('location-detail', args=[self.location1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Home')

    def test_retrieve_nonexistent_location(self):
        url = reverse('location-detail', args=[999]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_location(self):
        url = reverse('location-detail', args=[self.location2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Location.objects.count(), 1)

    def test_delete_nonexistent_location(self):
        url = reverse('location-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_duplicate_location(self):
        url = reverse('location-list')
        data = {'name': 'Home'}  # This name already exists
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
