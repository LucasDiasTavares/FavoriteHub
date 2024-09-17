import pdb

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from favoritehub.models import Favorite, Product, Client


class FavoriteViewSetTests(APITestCase):
    def setUp(self):
        # Criação de um usuário e produtos para testar
        self.user = User.objects.create_user(email='testuser@testuser.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.client1 = Client.objects.create(email='client1@example.com', name='Client One')
        self.client2 = Client.objects.create(email='client2@example.com', name='Client Two')

        self.product1 = Product.objects.create(title='Product 1', price=100.0)

        self.favorite_list = Favorite.objects.create(client=self.client1)

        # Nome do endpoint baseado no basename do router
        self.list_url = reverse('favorite-list')
        self.add_product_url = reverse('favorite-add-product', kwargs={'pk': self.favorite_list.id})
        self.remove_product_url = reverse('favorite-remove-product', kwargs={'pk': self.favorite_list.id})

    def test_get_favorites(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.favorite_list.id, [f['id'] for f in response.data['results']])

    def test_create_favorite_list(self):
        response = self.client.post(self.list_url, {'client': self.client2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.count(), 2)
        # Verifica se a lista foi criada, tenho 2 clientes, então deve ser 2 o resultado do count()

    def test_add_product_to_favorite_list(self):
        url = reverse('favorite-add-product', kwargs={'pk': self.favorite_list.id})
        response = self.client.post(url, {'product_id': self.product1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.product1, self.favorite_list.products.all())

    def test_add_nonexistent_product(self):
        url = reverse('favorite-add-product', kwargs={'pk': self.favorite_list.id})
        # ID de produto que não existe
        response = self.client.post(url, {'product_id': 9999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Product does not exist')

    def test_add_duplicate_product(self):
        # Adiciona o produto uma vez
        self.client.post(self.add_product_url, {'product_id': self.product1.id})
        response = self.client.post(self.add_product_url, {'product_id': self.product1.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Product already in the favorite list')

    def test_remove_product_from_favorite_list(self):
        # Adiciona o produto primeiro
        self.client.post(self.add_product_url, {'product_id': self.product1.id})
        response = self.client.post(self.remove_product_url, {'product_id': self.product1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.product1, self.favorite_list.products.all())

    def test_remove_nonexistent_product_from_favorite_list(self):
        response = self.client.post(self.remove_product_url,
                                    {'product_id': 9999})  # ID de produto que não existe na lista
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Product does not exist')
