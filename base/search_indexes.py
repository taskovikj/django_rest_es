from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import BlogPost


@registry.register_document
class BlogPostDocument(Document):
    class Index:
        name = 'blogposts'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    title = fields.TextField()
    content = fields.TextField()
    author = fields.ObjectField(properties={'username': fields.TextField()})
    pub_date = fields.DateField()

    class Django:
        model = BlogPost
