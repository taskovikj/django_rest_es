from elasticsearch_dsl import Document, Text, Date
from elasticsearch_dsl.connections import connections
from .models import Book, BlogPost

connections.create_connection(hosts=['localhost'])

class BookIndex(Document):
    title = Text()
    description = Text()

    class Index:
        name = 'book_index'



