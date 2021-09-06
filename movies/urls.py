from django.urls import path

from .views import GetRecommendation

urlpatterns = [
    path('recommend/', GetRecommendation.as_view(), name='get-mbti'),

]
