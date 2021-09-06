from rest_framework import views
from rest_framework.response import Response

from .utils import get_mbti_from_twitter_id


class GetMbti(views.APIView):

    def get(self, request, format=None):
        twitter_id = request.query_params.get('id')
        mbti = get_mbti_from_twitter_id(twitter_id)

        if mbti == 'INVALID':
            return Response(data={
                'error': 'could not find or fetch your twitter page'
            }, status=400)

        if mbti == 'NEED_MORE':
            return Response(data={
                'error': 'your tweets are not enough'
            }, status=400)

        return Response(data={
           'mbti': mbti
        }, status=200)
