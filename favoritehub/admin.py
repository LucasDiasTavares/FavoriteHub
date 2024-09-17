from django.contrib import admin
from .models import Client, Product, Favorite

admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Favorite)
