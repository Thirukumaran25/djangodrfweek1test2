from rest_framework import serializers
from datetime import date
from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def validate_published_date(self, value):
        current_year = date.today().year
        if value.year > current_year:
            raise serializers.ValidationError("Published year cannot be in the future.")
        return value
