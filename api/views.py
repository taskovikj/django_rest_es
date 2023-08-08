from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Items, Book, Author
from .serializers import ItemSerializer, BookSerializer, AuthorSerializer


@api_view(['GET'])
def getData(requests):
    person = {'name':'Branislav','age':'22'}
    items = Items.objects.all()
    serializer = ItemSerializer(items,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addData(requests):
    serializer = ItemSerializer(data=requests.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def getAuthors(requests):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_author(request):
    serializer = AuthorSerializer(data=requests.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def getBooks(requests):
    books = Book.objects.all()
    serializer = BookSerializer(books,many=True)
    return Response(serializer.data)




