from django.core.management.base import BaseCommand
from django_seed import Seed
from books.models import Book, Review, Sale
from authors.models import Author

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # 50 Authors
        seeder.add_entity(Author, 50, {
            'name': lambda x: seeder.faker.name(),
            'date_birth': lambda x: seeder.faker.date_of_birth(),
            'origin_country': lambda x: seeder.faker.country(),
            'description': lambda x: seeder.faker.paragraph(),
        })
        # 300 Books

        seeder.add_entity(Book, 300, {
            'name': lambda x: seeder.faker.catch_phrase(),
            'summary': lambda x: seeder.faker.paragraph(),
            'date_of_pub': lambda x: seeder.faker.date(),
            'num_sales': lambda x: seeder.faker.unique.random_int(min=10, max=1000000),
            'author': lambda x: Author.objects.get(pk=seeder.faker.random_int(min=1, max=50))
        })

        # 1-10 reviews per book

        for book in Book.objects.all():
            seeder.add_entity(Review, seeder.faker.random_int(min=1, max=10), {
                'book': book,
                'review': lambda x: seeder.faker.paragraph(),
                'score': lambda x: seeder.faker.random_int(min=1, max=10),
                'num_upvotes': lambda x: seeder.faker.random_int(min=0, max=1000)
            })

        # 5 Years of sales per book

        for book in Book.objects.all():
            used_years = set()

            def generate_unique_year():
                while True:
                    year = seeder.faker.random_int(min=2010, max=2023)
                    if year not in used_years:
                        used_years.add(year)
                        return year

            seeder.add_entity(Sale, 5, {
                'book': book,
                'year': generate_unique_year(),
                'sales': lambda x: seeder.faker.random_int(min=100, max=10000)
            })
            book.num_sales = sum(sale.sales for sale in book.sales.all())
            book.save()

        inserted_pks = seeder.execute()

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database with {len(inserted_pks)} instances'))
