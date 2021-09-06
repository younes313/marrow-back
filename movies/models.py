from bs4 import BeautifulSoup
import requests
import numpy as np

from django.db import models
from django.conf import settings

from .utils import number_converter
from users.utils import generate_mbti


class Movie(models.Model):
    name = models.CharField(max_length=250)
    imdb_id = models.CharField(max_length=100)
    imdb_rate = models.FloatField(null=True)
    imdb_rate_number = models.BigIntegerField(null=True)
    budget = models.BigIntegerField(null=True)
    gross = models.BigIntegerField(null=True)
    year = models.IntegerField(null=True)
    description = models.TextField(null=True)
    image_link = models.URLField(null=True)

    keywords = models.ManyToManyField('movies.keyword')
    genres = models.ManyToManyField('movies.genre')

    def get_gross_budget_ratio(self):
        if self.gross and self.budget:
            return self.gross / self.budget
        return 0.01

    def generate_data(self):
        result = [self.imdb_rate, self.imdb_rate_number or 0.12, self.get_gross_budget_ratio()]
        genres = [genre.name.lower() for genre in self.genres.all()]
        for genre in self.get_genre_list():
            result.append(1 if genre in genres else 0)
        return result

    def genre_list(self):
        return [genre.name for genre in self.genres.all()]

    def keyword_list(self):
        return [keyword.name for keyword in self.keywords.all()]

    @staticmethod
    def get_genre_list():
        return ['drama', 'news', 'thriller', 'biography', 'sport', 'horror', 'animation', 'history', 'action',
                'mystery', 'short', 'film-noir', 'musical', 'war', 'crime', 'family', 'adventure', 'music', 'sci-fi',
                'western', 'comedy', 'romance', 'documentary', 'fantasy']

    @classmethod
    def get_recommended_movies(cls, mbti):
        all_movies = cls.objects.filter().order_by('?')
        result = []
        for movie in all_movies:
            if cls.check_favor(movie.imdb_id, mbti)[1]:
                result.append(movie)
                if len(result) >= 4:
                    break
        return result

    @property
    def imdb_link(self):
        return f'https://www.imdb.com/title/tt{self.imdb_id}/'

    def update_fields_from_imdb(self, force=False):
        if not force and self.imdb_rate and self.imdb_rate_number and self.image_link and self.description:
            return
        try:
            url = f'https://www.imdb.com/title/tt{self.imdb_id}/'
            response = requests.get(url)
            soup = BeautifulSoup(response.text)
            self.name = soup.find('meta', property='og:title')['content'].replace(' - IMDb', '')
            self.imdb_rate = soup.find('span', class_='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV').text

            rate_count_string = soup.find('div',
                                          class_='AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3 jkCVKJ').text
            self.imdb_rate_number = number_converter(rate_count_string)
            self.image_link = soup.find('meta', property='og:image')['content']
            self.description = soup.find('meta', property='og:description')['content']
            genres = soup.find('div', class_='ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL')
            current_genres = [genre.name for genre in self.genres.all()]
            for genre in genres:
                genre_name = genre.find('span', class_='ipc-chip__text').text
                if genre_name not in current_genres:
                    self.genres.add(Genre.objects.get_or_create(name=genre_name)[0])

            try:
                box_office = soup.find_all('li',
                                           class_='ipc-metadata-list__item BoxOffice__MetaDataListItemBoxOffice-sc-40s2pl-2 gwNUHl')
                for box in box_office:
                    label = box.find('span', class_='ipc-metadata-list-item__label').text
                    if label == 'Gross worldwide':
                        self.gross = int(
                            box.find('span', class_='ipc-metadata-list-item__list-content-item').text.split()[0][
                            1:].replace(',', ''))
                    elif label == 'Budget':
                        self.budget = int(
                            box.find('span', class_='ipc-metadata-list-item__list-content-item').text.split()[0][
                            1:].replace(',', ''))
            except Exception as e:
                with open('./logs.txt', 'a') as file:
                    file.write(str(e))

        except Exception as e:
            with open('./logs.txt', 'a') as file:
                file.write(str(e))
        self.save()

    @classmethod
    def check_favor(cls, imdb_id, mbti):
        model = settings.MOVIE_PREDICT_MODEL
        movie, created = cls.objects.get_or_create(imdb_id=imdb_id)
        print(created)
        print(movie.generate_data() + generate_mbti(mbti))
        if created or True:
            movie.update_fields_from_imdb(force=True)
        result = model.predict([list(map(str, movie.generate_data() + generate_mbti(mbti)))])
        return movie, True if result[0] else False


class Keyword(models.Model):
    name = models.CharField(max_length=250)


class Genre(models.Model):
    name = models.CharField(max_length=250)


class UserRating(models.Model):
    movie = models.ForeignKey('movies.movie', on_delete=models.DO_NOTHING)

    twitter_id = models.CharField(max_length=250)
    user_mbti = models.CharField(max_length=10)
    user_rate = models.IntegerField()
