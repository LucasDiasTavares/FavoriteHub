import pdb

from rest_framework.test import APITestCase
from rest_framework import status
from favoritehub.models import Client
from authentication.models import User


class ClientViewSetTests(APITestCase):
    def setUp(self):
        # Cria um usuário
        self.user = User.objects.create_user(email='testuser@testuser.com', password='testpassword')

        # Cria clientes
        self.client1 = Client.objects.create(email='client1@example.com', name='Client One')
        self.client2 = Client.objects.create(email='client2@example.com', name='Client Two')

        # URL base para os testes
        self.url = '/api/clients/'

        # Autentica o usuário
        self.client.force_authenticate(user=self.user)

    def test_list_clients(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], 'Client One')
        self.assertEqual(response.data['results'][1]['name'], 'Client Two')

    def test_create_client(self):
        data = {
            'email': 'newclient@example.com',
            'name': 'New Client'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 3)
        self.assertEqual(Client.objects.get(id=response.data['id']).name, 'New Client')

    def test_create_client_with_duplicate_email(self):
        data = {
            'email': 'client1@example.com',
            'name': 'Duplicate Client'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_update_client(self):
        update_url = f'{self.url}{self.client1.id}/'
        data = {
            'name': 'Updated Client One'
        }
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.name, 'Updated Client One')

    def test_delete_client(self):
        delete_url = f'{self.url}{self.client2.id}/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 1)
        self.assertFalse(Client.objects.filter(id=self.client2.id).exists())
