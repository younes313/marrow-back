from django.urls import path

from .views import GetMbti

urlpatterns = [
    path('mbti/', GetMbti.as_view(), name='get-mbti'),

]
