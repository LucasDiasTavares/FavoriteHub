from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ClientViewSet, ProductListCreateAPIView, FavoriteViewSet

router = DefaultRouter()

router.register(r'clients', ClientViewSet, basename='client')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
]
