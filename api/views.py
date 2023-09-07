from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Items, Book, Author, Category
from .serializers import ItemSerializer, BookSerializer, AuthorSerializer
from base.views import blog_detail_view


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
    serializer = AuthorSerializer(data=request.data)
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


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def search_items(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('categories')
    all_categories = Category.objects.all()
    search_results = []
    print(selected_category)

    if query or selected_category:
        search = BlogPostDocument.search().sort("-pub_date")

        if query:
            search = search.query("wildcard", title=f"*{query}*")

        if selected_category:
            search = search.filter('term', category__name=selected_category)

        search_response = search.execute()
        search_results = search_response.hits

    print(search_results)


    return render(request, 'search.html', {'results': search_results, 'query': query,'categories':all_categories})
















