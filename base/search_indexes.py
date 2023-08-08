from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Items


@registry.register_document
class ItemsDocument(Document):
    class Index:
        name = 'items'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    name = fields.TextField()
    created = fields.DateField()

    class Django:
        model = Items
