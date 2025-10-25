import factory
import random
from product.models import Product, Category


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")
    slug = factory.Faker("slug")
    description = factory.Faker("sentence")
    active = factory.LazyFunction(lambda: random.choice([True, False]))

    class Meta:
        model = Category
        django_get_or_create = ('slug',)


class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")
    price = factory.Faker("pyint", min_value=10, max_value=1000)
    active = True

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)

    class Meta:
        model = Product
