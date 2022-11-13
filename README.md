# Show Analysis

I've decided to scrape reviews for movies and series (along with general info about shows) from popular online database of information related to movies and television series and use this data to practice different data science techniques and improve my skills.  

Here is the plan of what I'm going to do:

- [Show Analysis](#show-analysis)
  - [Parsing web-pages to collect the datasets](#parsing-web-pages-to-collect-the-datasets)
  - [Data Preprocessing](#data-preprocessing)
    - [Anonymization](#anonymization)
    - [Transformation](#transformation)
    - [Exploratory Data Analysis](#exploratory-data-analysis)
  - [Building ML applications](#building-ml-applications)
    - [Sentiment analysis of show reviews](#sentiment-analysis-of-show-reviews)
      - [Baseline: TF-IDF + Logistic Regression](#baseline-tf-idf--logistic-regression)
      - [Pretrained models](#pretrained-models)
        - [Dostoevsky](#dostoevsky)
        - [HuggingFace models](#huggingface-models)
    - [Show recommendation system](#show-recommendation-system)
    - [Text generation](#text-generation)
  - [Data Analytics](#data-analytics)
    - [Research on the quality of localization of movie titles](#research-on-the-quality-of-localization-of-movie-titles)

## Parsing web-pages to collect the datasets

The first step is collecting data. I've scraped information about top-1000 movies and top-1000 series.  
To learn more about scraped data and how exactly it was done [go here](https://github.com/Extremesarova/shows_analysis/tree/main/shows_analysis/code/parsing_pages).

## Data Preprocessing

### Anonymization

### Transformation

### Exploratory Data Analysis

## Building ML applications

### [Sentiment analysis of show reviews](https://github.com/Extremesarova/shows_analysis/tree/main/shows_analysis/notebooks/3_sentiment_analysis)

The goal of this analysis is to:

- Get hands-on experience with packages and tools for analyzing texts (`natasha`, `nltk`, `spacy`, `rnnmorph`, `pymorphy2`)
- Investigate available pretrained models (`wor2vec`, `fasttext`, `navec`, models from sber, deeppavlov and others)
- Learn how to fine-tune `BERT`-like models for classification tasks

#### [Baseline: TF-IDF + Logistic Regression](https://nbviewer.org/github/Extremesarova/shows_analysis/blob/main/shows_analysis/notebooks/3_sentiment_analysis/01_baseline.ipynb)

As a baseline, I've decided to choose a simple combination of TF-IDF for text vectorization and Logistic Regression for classification.  

The micro F1 score is `0.795` for baseline. I think that it is a very strong baseline.

#### Pretrained models

TODO

##### [Dostoevsky](https://nbviewer.org/github/Extremesarova/shows_analysis/blob/main/shows_analysis/notebooks/3_sentiment_analysis/02_a_pretrained_dostoevsky.ipynb)

TODO

##### [HuggingFace models](https://nbviewer.org/github/Extremesarova/shows_analysisblob/main/shows_analysis/notebooks/analysis/3_sentiment_analysis02_b_pretrained_huggingface.ipynb)

TODO

### Show recommendation system

TODO

### Text generation

TODO

1. Movie Titles
2. Movie Reviews

## Data Analytics

### Research on the quality of localization of movie titles

The aim of this study was to find out:

- How similar are Russian titles and original titles in general?
- Is it possible to split dissimilar pairs (Russian title :: original title) into groups according to the root cause?
  
To learn about results [go here](https://github.com/Extremesarova/shows_analysis/tree/main/shows_analysis/notebooks/1_title_localization_analysis).
