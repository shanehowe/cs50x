SELECT     movies.title,
           ratings.rating
FROM       ratings
INNER JOIN movies
where      movies.id = ratings.movie_id
AND        year = 2010
ORDER BY   rating DESC, title ASC;