import factory
import factory.random

factory.random.reseed_random('teahouse')

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