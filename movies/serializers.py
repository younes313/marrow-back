from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    keyword_list = serializers.SerializerMethodField()
    genre_list = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'name', 'imdb_id', 'imdb_link', 'imdb_rate', 'imdb_rate_number', 'budget', 'gross', 'year', 'image_link',
            'description', 'keyword_list', 'genre_list'
        )

    def get_keyword_list(self, obj):
        keywords = obj.keyword_list()
        return keywords[:min(5, len(keywords))] if keywords else []

    def get_genre_list(self, obj):
        return obj.genre_list()
