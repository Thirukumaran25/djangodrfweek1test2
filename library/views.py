from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer



class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Book.objects.all()
        author_name = self.request.query_params.get('author')
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
        return queryset
    

class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def author_list_create(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
