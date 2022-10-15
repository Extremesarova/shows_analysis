# Parsing Data

I've scraped information about top-1000 movies and top-1000 series in Russia.  

## Movies

* Info:
  * Dimensions: (984, 43)
  * Columns:
    * Show ID
    * Russian Title
    * Original Title
    * Actors and Voice Actors
    * Show Info (year, country, genre, slogan, director, scriptwriter, producer, operator, composer, artist, cut, budget, us box office, world box office, viewers, Russian box office, Russian premiere, world premiere, DVD release, blue ray release, age rating, MPAA rating, duration, digital release, marketing, platform, rerelease, film director)
    * rating kinopoisk, rating count kinopoisk, rating IMDB, rating count IMDB
    * synopsis
    * world critic's percentage, world critic's star value, world critic's number of reviews, Russian critic's percentage, Russian critic's number of reviews
* Reviews:
  * Dimensions: (171094, 8)
  * Target class values: `good` (123379), `neutral` (26059), `bad` (21656)
  * Columns:
    * show ID
    * username
    * date and time
    * sentiment
    * subtitle
    * review body
    * usefulness ratio
    * direct link to the review

## Series

* Info:
  * Dimensions: (978, 40)
  * Columns: the same as in movies (without viewers, marketing and rerelease columns)
* Reviews:
  * Dimensions: (35643, 8)
  * Target class values: `good` (25540), `neutral` (5157), `bad` (4946)
  * Columns: the same as in movies
