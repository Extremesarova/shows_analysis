# Parsing Data

I've scraped information about top-1000 movies and top-1000 series in Russia and divided the data into 4 datasets:

| Dataset Name  | Dimensions    |  Main columns|
| ------------- | ------------- |------------- |
| Movie Info  | (984, 43)  |Show ID, Russian Title, Original title, Actors, Show Info, Ratings, Synopsis, Critics' Scores  |
| Movie Reviews  | (171094, 8)  |Show ID, Date and Time, Sentiment, Review Subtitle, Review, Usefulness of Review  |
| Series Info  | (978, 40)  |Show ID, Russian Title, Original title, Actors, Show Info, Ratings, Synopsis, Critics' Scores  |
| Series Reviews  | (35643, 8)  |Show ID, Date and Time, Sentiment, Review Subtitle, Review, Usefulness of Review  |

Overall, I've got `206 737` **reviews** and `1962` **shows**.

Code to perform parsing can be found here:

- [Main file](https://github.com/Extremesarova/shows_analysis/blob/main/shows_analysis/code/parsing_pages/parsing.py) to start parsing process (with multiprocessing)
- [Dataobjects](https://github.com/Extremesarova/shows_analysis/tree/main/shows_analysis/code/parsing_pages/dataobjects) to represent review and show info abstractions
- [Parsers](https://github.com/Extremesarova/shows_analysis/tree/main/shows_analysis/code/parsing_pages/parsers) to parse web-pages
- [HTML reader](https://github.com/Extremesarova/shows_analysis/blob/main/shows_analysis/code/parsing_pages/reading/html_reader.py) to read the page
- [Utils](https://github.com/Extremesarova/shows_analysis/blob/main/shows_analysis/code/utils/parsing_utils.py)
