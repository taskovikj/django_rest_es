from rest_framework import serializers
from base.models import Items, Book, Author

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'