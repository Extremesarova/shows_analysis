# Parsing Data

I've scraped information about top-1000 movies and top-1000 series in Russia and separated the data into four datasets:

| Dataset Name  | Dimensions    |  Main columns|
| ------------- | ------------- |------------- |
| Movie Info  | (984, 43)  |Show ID, Russian Title, Original title, Actors, Show Info, Ratings, Synopsis, Critics' Scores  |
| Movie Reviews  | (171094, 8)  |Show ID, Date and Time, Sentiment, Review Subtitle, Review, Usefulness of Review  |
| Series Info  | (978, 40)  |Show ID, Russian Title, Original title, Actors, Show Info, Ratings, Synopsis, Critics' Scores  |
| Series Reviews  | (35643, 8)  |Show ID, Date and Time, Sentiment, Review Subtitle, Review, Usefulness of Review  |
