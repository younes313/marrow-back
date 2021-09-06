from rest_framework import views
from rest_framework.response import Response

from .serializers import MovieSerializer
from .models import Movie


class GetRecommendation(views.APIView):

    def get(self, request, format=None):
        mbti = request.query_params.get('mbti', None)
        imdb_id = request.query_params.get('movie_id', None)

        the_movie, users_like = None, None
        if imdb_id:
            the_movie, users_like = Movie.check_favor(imdb_id, mbti)

        recommended_movies = Movie.get_recommended_movies(mbti)
        for movie in recommended_movies:
            movie.update_fields_from_imdb()
        return Response(data={
                'recommendations': MovieSerializer(recommended_movies, many=True).data,
                'the_movie': MovieSerializer(the_movie).data if the_movie else the_movie,
                'the_movie_result': users_like
        }, status=200)
