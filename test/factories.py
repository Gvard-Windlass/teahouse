import factory
import factory.random

factory.random.reseed_random('teahouse')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalogue.Product'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'test product %d' % n)
    price = factory.Faker('pyfloat', positive=True)
    description = factory.Faker('paragraph', nb_sentences=5)
    product_type = 'Misc'


class TeaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalogue.Tea'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'test tea №%d' % n)
    price = factory.Faker('pyfloat', positive=True)
    image = factory.Sequence(lambda n: 'product_images/black%d.jpg' % n)
    amount = factory.Faker('pyint')
    description = factory.Faker('paragraph', nb_sentences=5)
    product_type= 'Tea'
    tea_type = 'Black'
    tea_year = factory.Faker('year')


class UtensilFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalogue.Utensil'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'test utensil %d' % n)
    price = factory.Faker('pyfloat', positive=True)
    image = factory.Sequence(lambda n: 'product_images/cup%d.jpg' % n)
    amount = factory.Faker('pyint')
    description = factory.Faker('paragraph', nb_sentences=5)
    product_type= 'Utensil'
    utensil_type = 'Cup'
    utensil_material = 'Ceramic'


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'articles.Article'
        django_get_or_create = ('title',)

    author = factory.Faker('random_element', elements=('alice', 'bob', 'peter'))
    title = factory.Sequence(lambda n: 'test article %d' % n)
    summary = factory.Faker('paragraph', nb_sentences=5)
    body = factory.Faker('paragraph', nb_sentences=20)