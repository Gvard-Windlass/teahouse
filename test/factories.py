import factory
import factory.random
from django.contrib.auth.models import User
from django.conf import settings

factory.random.reseed_random("teahouse")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = "gvard"
    password = "Bk7^31&3LDXt"
    email = "test@example.com"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "catalogue.Product"
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "test product %d" % n)
    price = factory.Faker("pyfloat", positive=True)
    description = factory.Faker("paragraph", nb_sentences=5)
    product_type = "Misc"


class TeaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "catalogue.Tea"
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "test tea №%d" % n)
    price = factory.Faker("pyfloat", positive=True)
    image = factory.Sequence(lambda n: "product_images/red%d.jpg" % n)
    amount = factory.Faker("pyint", min_value=settings.AMOUNT_STEP)
    description = factory.Faker("paragraph", nb_sentences=5)
    product_type = "Tea"
    tea_type = "Red"
    tea_year = factory.Faker("year")


class UtensilFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "catalogue.Utensil"
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "test utensil %d" % n)
    price = factory.Faker("pyfloat", positive=True)
    image = factory.Sequence(lambda n: "product_images/cup%d.jpg" % n)
    amount = factory.Faker("pyint", min_value=1)
    description = factory.Faker("paragraph", nb_sentences=5)
    product_type = "Utensil"
    utensil_type = "Cup"
    utensil_material = "Ceramic"


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "articles.Article"
        django_get_or_create = ("title",)

    author = factory.Faker("random_element", elements=("alice", "bob", "peter"))
    title = factory.Sequence(lambda n: "test article %d" % n)
    summary = factory.Faker("paragraph", nb_sentences=5)
    body = factory.Faker("paragraph", nb_sentences=20)
