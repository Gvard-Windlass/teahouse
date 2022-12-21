import factory
import factory.random
from faker import Faker

factory.random.reseed_random('teahouse')
fake = Faker()

class TeaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalogue.Tea'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'test tea №%d' % n)
    price = fake.pyfloat(positive=True)
    image = factory.Sequence(lambda n: 'product_images/black%d.jpg' % n)
    amount = fake.pyint()
    description = fake.paragraph(nb_sentences=5)
    product_type= 'Tea'
    tea_type = 'Black'
    tea_year = fake.year()