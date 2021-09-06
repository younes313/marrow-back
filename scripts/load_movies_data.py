from csv import reader
import re

from movies.models import Movie, Genre, Keyword


with open('scripts/data/final_data.csv', 'r') as file:
    csv_reader = reader(file)

    for row in list(csv_reader)[1:]:
        movie, created = Movie.objects.get_or_create(
            name=row[3],
            imdb_id=row[2],
            imdb_rate=row[7] or None,
            imdb_rate_number=int(float(row[8])) if row[8] else None,
            budget=row[9] or None,
            gross=row[10] or None,
            year=re.search(".*\((\d{4})\).*", row[3]).group(1)
        )
        if created:
            for keyword in row[4].split('|'):
                movie.keywords.add(Keyword.objects.get_or_create(name=keyword)[0])

            for genre in row[5].split('|'):
                movie.genres.add(Genre.objects.get_or_create(name=genre)[0])
