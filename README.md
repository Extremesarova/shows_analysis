# Shows Parsing

I've decided to scrape reviews for movies and series (along with general info about shows) from popular online database of information related to movies and television series and use this data to practice different data science techniques and improve my skills.  

## Parsing web-pages to collect the datasets

I've scraped information about top-1000 movies and top-1000 series in Russia and divided the data into 4 datasets:

| Dataset Name  | Dimensions    |  Main columns|
| ------------- | ------------- |------------- |
| Movie Info  | (984, 43)  |Show ID, Russian Title, Original title, Actors, Show Info, Ratings, Synopsis, Critics' Scores  |
| Movie Reviews  | (171094, 8)  |Show ID, Date and Time, Sentiment, Review Subtitle, Review, Usefulness of Review  |
| Series Info  | (978, 40)  |Show ID, Russian Title, Original title, Actors, Show Info, Ratings, Synopsis, Critics' Scores  |
| Series Reviews  | (35643, 8)  |Show ID, Date and Time, Sentiment, Review Subtitle, Review, Usefulness of Review  |

Overall, I've got `206 737` **reviews** and `1962` **shows**.

Code to perform parsing can be found here:

- [Parsing](https://github.com/Extremesarova/shows_analysis/blob/main/shows_analysis/code/parsing_pages/parsing.py) to start parsing process (with multiprocessing)
- [Dataobjects](https://github.com/Extremesarova/shows_analysis/tree/main/shows_analysis/code/parsing_pages/dataobjects) to represent review and show info abstractions
- [Parsers](https://github.com/Extremesarova/shows_analysis/tree/main/shows_analysis/code/parsing_pages/parsers) to parse web-pages
- [HTML Reader](https://github.com/Extremesarova/shows_analysis/blob/main/shows_analysis/code/parsing_pages/reading/html_reader.py) to read the page
- [Parsing Utils](https://github.com/Extremesarova/shows_analysis/blob/main/shows_analysis/code/utils/parsing_utils.py)

## Set-up

```bash
pip install -e .
python src/parsing_pages/parsing.py data movies 12
python src/parsing_pages/parsing.py data series 12
```
