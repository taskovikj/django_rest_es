from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Items, Book, Author, Category
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



from django.shortcuts import render
from base.search_indexes import ItemsDocument, BlogPostDocument
from elasticsearch_dsl import Document, Text, Keyword
def search_items(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    categories = Category.objects.all()

    # Create a search object
    search = BlogPostDocument.search()

    if query:
        query = query.strip()  # Remove leading/trailing spaces
        search = search.query("wildcard", category=category)

    if category:
        search = search.filter('term', category=category)

    # Execute the search
    search_response = search.execute()
    search_results = search_response.hits

    return render(request, 'search.html', {'results': search_results, 'all_categories': categories})














