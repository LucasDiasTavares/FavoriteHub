from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Client, Product, Favorite
from .serializers import ClientSerializer, ProductSerializer, FavoriteSerializer


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Favorite.objects.all().order_by('id')
    serializer_class = FavoriteSerializer
    http_method_names = ['head', 'get', 'post', 'delete']

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'client': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the client to create the favorite list'
                )
            },
            required=['client']
        ),
        responses={
            200: openapi.Response('Favorite list created'),
            400: openapi.Response(
                description='Invalid request data',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['products'] = []
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the product to add to the favorite list'
                )
            },
            required=['product_id']
        ),
        responses={
            200: openapi.Response('Product added'),
            400: openapi.Response('Product does not exist or validation error')
        }
    )
    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        favorite_list = self.get_object()
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)

            if favorite_list.products.filter(id=product_id).exists():
                return Response({'error': 'Product already in the favorite list'}, status=status.HTTP_400_BAD_REQUEST)

            favorite_list.add_product(product)
            return Response({'status': 'product added'})

        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the product to remove from the favorite list'
                )
            },
            required=['product_id']
        ),
        responses={
            200: openapi.Response('Product removed'),
            400: openapi.Response('Product does not exist or not in the favorite list')
        }
    )
    @action(detail=True, methods=['post'])
    def remove_product(self, request, pk=None):
        favorite_list = self.get_object()
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)

            if not favorite_list.products.filter(id=product_id).exists():
                return Response({'error': 'Product not in the favorite list.'}, status=status.HTTP_400_BAD_REQUEST)

            favorite_list.remove_product(product)
            return Response({'status': 'product removed'})

        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=400)

        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
