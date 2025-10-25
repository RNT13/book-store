from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    @property
    def total(self):
        return sum(p.price for p in self.products.all())
