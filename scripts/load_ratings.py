from csv import reader

from movies.models import UserRating, Movie


with open('scripts/data/final_data.csv', 'r') as file:
    csv_reader = reader(file)

    for row in list(csv_reader)[1:]:
        UserRating.objects.create(
            movie=Movie.objects.get(imdb_id=row[2]),
            twitter_id=row[0],
            user_mbti=row[1],
            user_rate=row[6]
        )

