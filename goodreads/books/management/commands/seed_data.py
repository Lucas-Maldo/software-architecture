from django.core.management.base import BaseCommand
from django_seed import Seed
from books.models import Book, Review, Sale
from authors.models import Author

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # 50 Authors
        seeder.add_entity(Book, 300, {
            'name': lambda x: seeder.faker.name(),
            'summary': lambda x: seeder.faker.paragraph(),
            'date_of_pub': lambda x: seeder.faker.date(),
            'num_sales': lambda x: seeder.faker.unique.random_int(min=10, max=1000000),
        })
        # 300 Books

        # 1-10 reviews per book

        # 5 Years of sales per book

        inserted_pks = seeder.execute()

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database with {len(inserted_pks)} instances'))
