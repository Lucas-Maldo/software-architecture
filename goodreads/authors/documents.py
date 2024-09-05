from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Author


@registry.register_document
class AuthorDocument(Document):
    class Index:
        name = 'authors'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Author
        fields = [
            'name',
            'description'
        ]