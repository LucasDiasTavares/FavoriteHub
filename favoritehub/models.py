from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Avg
from simple_history.models import HistoricalRecords


class Client(models.Model):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    history = HistoricalRecords()

    def __str__(self):
        return self.title

    def average_rating(self):
        return self.reviews.aggregate(average_rating=Avg('rating'))['average_rating'] or None


class Favorite(models.Model):
    client = models.OneToOneField(
        Client, on_delete=models.CASCADE, related_name='favorite_list')
    products = models.ManyToManyField(
        Product, blank=True, related_name='favorite_clients')

    history = HistoricalRecords()

    def __str__(self):
        return f'Favorites list of {self.client.name}'

    def add_product(self, product):
        self.products.add(product)

    def remove_product(self, product):
        self.products.remove(product)

    def save(self, *args, **kwargs):
        if not self.pk and Favorite.objects.filter(client=self.client).exists():
            raise ValidationError("Client already has a favorite list.")
        super().save(*args, **kwargs)
