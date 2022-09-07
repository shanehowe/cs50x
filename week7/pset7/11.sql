SELECT people.name
FROM people
INNER JOIN ratings
INNER JOIN directors
INNER JOIN movies
WHERE directors.person_id = people.id
AND directors.movie_id = movies.id
AND ratings.movie_id = movies.id
AND ratings.rating >= 9.0;