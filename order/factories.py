import factory
from django.contrib.auth.models import User
from order.models import Order


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    username = factory.Faker("user_name")

    class Meta:
        model = User
        django_get_or_create = ('username',)


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.products.add(product)

    class Meta:
        model = Order
